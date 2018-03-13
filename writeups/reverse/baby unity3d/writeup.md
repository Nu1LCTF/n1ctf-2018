## baby unity3d

This app is compiled with "[il2cpp](https://docs.unity3d.com/Manual/IL2CPP.html)", which can converts IL code from scripts and assemblies into C++ code.



In many times,we can use tools to recover the symbols in the libil2cpp.so, like [Il2CppDumper](https://github.com/Perfare/Il2CppDumper). 



But this time it doesn't work, global-metadata.dat is encrypted.So we have to find the decryption function. MetadataCache::Initialize() is the function which loads global-metadata.dat, but I encrypt the string "global-metadata.dat" :P . We can still find the function from Runtime::Init().



The encryption function can be found in MetadataLoader::LoadMetadataFile(), it's a simple xor algorithm.



### easier solution

dump the memory and search essential string.



Finally, it's a simple AES to verify the flag.Find the iv and key then get the flag~.







