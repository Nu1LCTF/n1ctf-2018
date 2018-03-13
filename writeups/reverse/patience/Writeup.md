## Writeup of challenge 'patience'

This is a pretty straight-forward challenge. What you need to do is to understand the simple algorithm inside the challenge binary and try to find a optimized one to print out the flag faster.

The original intention of this challenge is to let players learn about [Cmm](https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/Cmm), so I didn't give out the compiled binary file in the first version of this challenge. But I decided to distribute the binary because (1) my lack of knowledge about GHC (I was afraid of making confusions), (2) most players relies on dynamic analysis when doing reversing tasks. 

Finally, what you get from the challenge attachment is a stripped binary (so you can't use [this awesome tool](https://github.com/gereeter/hsdecomp)) and a compiler intermediate dump of the Cmm. I really suggest you to read the source of [GHC](https://github.com/ghc/ghc) to have a grasp of how functional programming languages are compiled into native binary (maybe GHC is a little special though :p).

