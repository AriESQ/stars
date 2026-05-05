This is the second part of a series introducing Bash programmers to Go. This part is about basics of writing CLI tools in Go. See the [first](https://github.com/go-monk/from-bash-to-go-part-i) part for the language building blocks.

# Our first CLI tool

Bash is often used to write small CLI tools and automation. Let's start with an example CLI tool that prints "hello" to terminal. The Bash version is pretty simple:

```bash
#!/bin/bash
echo hello
```

Now, let's implement a Go version. We start by creating a directory where the first version of our program will live. We also initialize a module in there:

```sh
$ mkdir -p hello/1
$ cd hello/1
$ go mod init hello
```

Since the program is not complex we don't have to think a lot about its design and can easily start with a test:

```go
// hello/1/hello_test.go
package hello_test

import (
	"hello"
	"testing"
)

func TestPrintExists(t *testing.T) {
	hello.Print()
}
```

We named the package `hello_test` instead of `hello`. This is possible and it allows for writing tests that use only the public API (identifiers starting with a capital letter) of the tested package as a real user would. Note that `*_test` packages are the sole exception to Go's standard rule that each source directory can contain only one package. In this test we just call the `Print` function from the `hello` package. Let's try and run the test:

```sh
$ go test
hello: no non-test Go files in ~/github.com/go-monk/from-bash-to-go-series/part-ii-cli-tools/hello/1
FAIL    hello [build failed]
```

Yes, we have not yet written the code we want to test. So let's do it:

```go
// hello/1/hello.go
package hello

func Print() {}
```

If we re-run the test

```sh
$ go test
PASS
ok      hello   0.570s
```

we can see that all is good now. Or is it? Well, something must be wrong because an empty function that does nothing at all (except that it exists) passes the test. So the *test* is obviously wrong. Now we need to start thinking a bit. What should be actually tested? 

## Making it testable

Okay, we want the function to print the string "hello" to terminal. How to test it except by looking at the terminal? In Bash the terminal is the standard output, i.e. the place where the stuff is written to by default. But we can redirect the standard output to a file or store it in a variable:

```bash
$ echo hello > /tmp/hello.txt
$ HELLO=$(echo hello)
```

In Go you can achieve similar functionality by using the standard library interface called [io.Writer](https://pkg.go.dev/io#Writer) (that is the `Writer` from the `io` package):

```go
// hello/2/hello.go
func PrintTo(w io.Writer) {
	s := "hello"
	w.Write([]byte(s))
}
```

We write (print) the string "hello" to `w` supplied as the function's argument. And since the argument (parameter more precisely) is an interface it can be multiple kinds of things. Or more precisely it can be any type that implements the `io.Writer` interface, i.e. has a function with the `Write(p []byte) (int, error)` signature attached.

There are many implementations of `io.Writer` in the standard library. Two of them are `bytes.Buffer` and `os.Stdout`. We can write to a bytes buffer in the test

```go
// hello/2/hello_test.go
func TestPrintToPrintsHelloToWriter(t *testing.T) {
	buf := new(bytes.Buffer)
	hello.PrintTo(buf) // writing to buffer
	want := "hello"
	got := buf.String()
	if want != got {
		t.Errorf("want %q, got %q", want, got)
	}
}
```

and to the standard output in the main function

```go
// hello/2/cmd/hello/main.go
func main() {
	hello.PrintTo(os.Stdout) // writing to STDOUT
}
```

Now we have a real test that we can rely on:

```sh
$ cd hello/2
$ go test
PASS
ok      hello   0.183s
```

As an exercise try to break the test so it doesn't pass.

We also added the `cmd` folder that holds the binary (command) to be used by the end user like this:

```sh
$ go install ./cmd/hello
$ hello
hello
```

## Decreasing complexity

Talking about the end user and looking at how the `PrintTo` function is called in `main`

```go
hello.PrintTo(os.Stdout)
```

we might think this is not ideal. Why should a user tell the function to print to standard output? Isn't it what most users want most of the time? Shouldn't it be the default behavior?

### Nil argument

But the `PrintTo` function *must* have an argument when called. So maybe we can use the approach that's used by the `http.ListenAndServe` standard library function; we use `nil` to indicate we want the default behaviour:

```go
// hello/3/hello.go
func PrintTo(w io.Writer) {
	if w == nil {
		w = os.Stdout
	}
	s := "hello"
	w.Write([]byte(s))
}
```

```go
// hello/3/cmd/hello/main.go
hello.PrintTo(nil)
```

Hmm, this works but still seems unnecessary complex.

### Global variable

We could remove the need for an argument altogether by using a global variable that would define where to write:

```go
// hello/4/hello.go
var Output io.Writer = os.Stdout
```

To change the default, you change the global variable:

```go
// hello/4/hello_test.go
hello.Output = new(bytes.Buffer)
hello.Print()
```

However, changing the state globally is always dangerous. For example, if we had multiple tests that would be running in parallel (using `testing.Parallel()` for example), changing the global variable from multiple functions at the same time could cause problems.

### A struct

A way to avoid the dangers of global variables is to create a custom variable type, usually based on a struct:

```go
// hello/5/hello.go
type Printer struct {
	Output io.Writer
}
```

Now you can have multiple variables of this type that won't affect each other:

```go
p1 := hello.Printer{Output: os.Stdout}
p2 := hello.Printer{Output: os.Stderr}
p1.Print() // prints to standard output
p2.Print() // prints to standard error
```

But we re-introduced the problem of having to define the default writer. To fix this we create a function called `NewPrinter` that sets the output to the default value:

```go
// hello/6/hello.go
func NewPrinter() *Printer {
	return &Printer{
		Output: os.Stdout,
	}
}
```

Note that now we use a *pointer* to `Printer`. This way we can change the default output by assigning to the `Output` field:

```go
// hello/6/cmd/hello/main.go
p := hello.NewPrinter()
p.Output = os.Stderr
p.Print()
```

# Getting more practical

Having done the obligatory hello (world) example let's turn to something more practical. We'll write a CLI tool to count duplicate lines in input. To be able to change the input we create a type called `counter` with the `input` field of the `io.Reader` type

```go
// count/1/count.go
type counter struct {
	input io.Reader
}
```

and attach a function (method) to it:

```go
func (c *counter) Lines() (map[string]int, error) {
	counts := make(map[string]int)
	input := bufio.NewScanner(c.input)
	for input.Scan() {
		counts[input.Text()]++
	}
	return counts, input.Err()
}
```

The Lines function counts duplicate lines by scanning the input line by line and keeping the count for each identical line in a map (of strings to integers).

## Optional parameter

Here's another pattern for having both a default value and being able to change it if needed. It's based on a function type - yeah, in Go we can define a custom type that is a function.

The `option` type below is a function with specific signature. And we define the `NewCounter` function to use the `option` type for its parameters. There can be zero or more of such parameters. This is called a variadic parameter and it's denoted by the `...` syntax:

```go
// count/1/count.go
type option func(*counter) error

func NewCounter(opts ...option) *counter {
	c := &counter{input: os.Stdin}
	for _, opt := range opts {
		opt(c) // NOTE: we ignore the error for now
	}
	return c
}
```

Now, let's define a function that returns an `option`:

```go
// count/1/count.go
func WithInput(input io.Reader) option {
	return func(c *counter) error {
		if input == nil {
			return errors.New("nil input reader")
		}
		c.input = input
		return nil
	}
}
```

## Command-line arguments

This `WithInput` function can be then used like this:

```go
// count/1/cmd/count/main.go
// ...
if len(os.Args) > 1 {
	// Input from file.
	file, err := os.Open(os.Args[1])
	// ...

	c := count.NewCounter(count.WithInput(file))
	counts, err = c.Lines()
} else {
	// Input from stdin.
	c := count.NewCounter()
	counts, err = c.Lines()
}
// ...
```

To find out what's `os.Args` we consult the documentation, for example like this:

```
$ go doc os.Args
package os // import "os"

var Args []string
    Args hold the command-line arguments, starting with the program name.
```

But if look at the `main` fuction in `count/1/cmd/count/main.go` the part handling the CLI arguments is a bit ugly. Let's hide it (abstract way) inside another function returning an `option`:

```go
// count/2/count.go
func WithInputFromArgs(args []string) option {
	return func(c *counter) error {
		if len(args) < 1 {
			return nil
		}
		f, err := os.Open(args[0])
		if err != nil {
			return err
		}
		c.input = f
		// NOTE: We are not closing the f and we take only the first
		// argument. See count/3/count.go for how to fix both these
		// shortcomings.
		return nil
	}
}
```

Now the main function gets easier on the eyes:

```go
// count/2/cmd/count/main.go
func main() {
	c, err := count.NewCounter(count.WithInputFromArgs(os.Args[1:]))
	if err != nil {
		log.Fatal(err)
	}
	counts, err := c.Lines()
	if err != nil {
		log.Fatal(err)
	}
	for line, n := range counts {
		fmt.Printf("%d\t%s\n", n, line)
	}
}
```

## Command-line flags

We saw how to handle the command line arguments. What about flags (also called options)?

This is the job of the `flag` standard library package that allows us to define usage message and one or more flags:

```go
// count/3/cmd/count/main.go
const usage = `Counts words (or lines) from stdin (or files).

Usage: count [-lines] [file...]`

func main() {
	flag.Usage = func() {
		fmt.Println(usage)
		flag.PrintDefaults()
	}
	lines := flag.Bool("lines", false, "count lines, not words")
	flag.Parse()
// ...
```

In the code above we defined the tool's documentation and a boolean flag. It looks like this from the user's perspective:

```
$ go run ./cmd/count -h
Counts words (or lines) from stdin (or files).

Usage: count [-lines] [file...]
  -lines
        count lines, not words
```

Nice and simple. We give it a try:

```sh
$ go run ./cmd/count -lines /etc/hosts /etc/networks | sort -n
```
