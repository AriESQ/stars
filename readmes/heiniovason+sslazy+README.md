# SSLazy

**warning:** I'm not an expert on windows security, and this code has not been used for any production system, but merely a proof of concept.

The program iterates all underlying nodes in both *StoreLocation* and *StoreName* when it tries to look up a given certificate. So if you plan on being inspired by this code then please do a security assessment of what impact this potentielly could lead to. I havent gotten around to do this, yet.


## How to (on windows)

1) Get a PKCS12 certificate from from https://badssl.com/download/
2) Install the certificate
3) Run --> mmc, find the certificate, and copy the thumbprint
4) Download and build the SSLazy project
5) Run Powershell, or Command Prompt as admin

```sh
$ cd \path\to\SSLazy\TryItOut\bin\Debug\netcoreapp3.1\
$ .\TryItOut.exe 41c36c33c7e336ddea4a1fc0b723b8e69cdcd80f https://client.badssl.com/

Certificate issued by: CN=BadSSL Client Root Certificate Authority, O=BadSSL, L=San Francisco, $ S=California, C=US
Configuring HttpClient ...
Calling server and waiting for response ...
StatusCode: 200, ReasonPhrase: 'OK', Version: 1.1, Content:
System.Net.Http.HttpConnectionResponseContent, Headers:
{
  Server: nginx/1.10.3
  Server: (Ubuntu)
  Date: Sat, 23 May 2020 18:12:59 GMT
  Connection: keep-alive
  ETag: "5e79513a-2af"
  Cache-Control: no-store
  Accept-Ranges: bytes
  Content-Type: text/html
  Content-Length: 687
  Last-Modified: Tue, 24 Mar 2020 00:15:54 GMT
}
```
