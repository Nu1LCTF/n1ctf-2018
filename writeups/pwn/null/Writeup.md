## Writeup for challenge 'null'

This is a relatively easy task I made for N1CTF 2018. I had a premonition of several players trying to use "House of orange" or similar techniques to solve it but finally stuck in a deadend, and.... it becomes true. :p

This challenge is pretty simple since generally it only does two things : malloc & read. Because it is simple so you are capable to exhaust all the possiblities. So what I want players to learn is, when you get stuck, you should try to seek other ways. People should know not only the usage of existing (public) methods,  but also the way to explore new methods.

The intended solution is corrupting `thread_arena`. See [x.py](./x.py) for more details.

Actually the "PadBlock" functionality is not present in the first version of this challenge, but considering network latency, I decided to add it no matter if it will become a subtle hint.

