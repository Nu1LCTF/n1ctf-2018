## Writeup for challenge 'memsafety'


This is a challenge compiled with an old version of `Rust` compiler. 

The first hint is meant to let everybody have a grasp of why the source code can't compile on newer versions of `Rust` compiler and leads them to the right direction.

After figuring out why the source can't compile, players can :

- Wandering around the broken part of the code and try to trigger the bug.
- Search for references of the fix (or issue) related to this problem.
- Do whatever they like to "learn" about the bug. :)

After players know there is a use-after-free bug, the common exploitation thoughts are to retake some important structures that can achieve memory read/write. So they need to study for some `Rust` internals.

Details can be found in : [x.py](./x.py)

## References

* [The origin of this challenge :)](https://github.com/rust-lang/rust/issues/37891)

