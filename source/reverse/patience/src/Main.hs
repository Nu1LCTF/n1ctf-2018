{-# LANGUAGE CPP #-}

module Main where

import System.IO
import Control.Monad

data FlagPos = Index !Int !Int

s0 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'\"()*+,-./:;<=>?@[\\]^_`{|}~"
s1 = "1vI{e[8Td]-nQ.7O\"bl(jq@<0Vy&Z3~\\ps,aD^;BN9JUoh|CE2_6!G\'rHuf>$S%MxgzKY4`c+WXA5F)mR}#PtL?*=i/:wk"
s2 = "Bp}i{XU%f$DR\\0<Lx=o\"Sl`bz)-e62|&JqFT!(C5yh;@u*.WaZ#Qv,?cr8wEm4_t19PH:j]>[NVMn7YGkK\'^/~OIdsA+3g"
s3 = "_r+#yh[Y)S8aXJwV&jv\"o=I(6>pg,f-M]qbN4\'EDKF\\t<3G%|$csPQm}~0@R;uU2z9iWB./HCk!{:Od^ZT7`Anl1e5L*x?"

f :: Int -> String
f 0 = s0
f x = s1 ++ (f $ subtract 1 x) ++ s2 ++ (f $ subtract 1 x) ++ s3

idx :: FlagPos -> Char
idx (Index depth index) = (f depth) !! index

flags = [
#include "flag.h"
 ]

main :: IO ()
main = forM_ (map idx flags) $ \c -> (putChar c >> hFlush stdout)
