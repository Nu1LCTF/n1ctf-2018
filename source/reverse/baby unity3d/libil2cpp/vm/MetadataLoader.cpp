#include "il2cpp-config.h"
#include "MetadataLoader.h"
#include "os/File.h"
#include "os/MemoryMappedFile.h"
#include "os/Mutex.h"
#include "utils/PathUtils.h"
#include "vm/Runtime.h"

using namespace il2cpp::os;
using namespace il2cpp::vm;


char* decrypt_file(char* src,size_t len)
{
    unsigned int table[] = {0xf83da249,0x15d12772,0x40c50697,0x984e2b6b,0x14ec5ff8,0xb2e24927,0x3b8f77ae,0x472474cd,0x5b0ce524,0xa17e1a31,0x6c60852c,0xd86ad267,0x832612b7,0x1ca03645,0x5515abc8,0xc5feff52,0xffffac00,0x0fe95cb6,0x79cf43dd,0xaa48a3fb,0xe1d71788,0x97663d3a,0xf5cffea7,0xee617632,0x4b11a7ee,0x040ef0b5,0x0606fc00,0xc1530fae,0x7a827441,0xfce91d44,0x8c4cc1b1,0x7294c28d,0x8d976162,0x8315435a,0x3917a408,0xaf7f1327,0xd4bfaed7,0x80d0abfc,0x63923dc3,0xb0e6b35a,0xb815088f,0x9bacf123,0xe32411c3,0xa026100b,0xbcf2ff58,0x641c5cfc,0xc4a2d7dc,0x99e05dca,0x9dc699f7,0xb76a8621,0x8e40e03c,0x28f3c2d4,0x40f91223,0x67a952e0,0x505f3621,0xbaf13d33,0xa75b61cc,0xab6aef54,0xc4dfb60d,0xd29d873a,0x57a77146,0x393f86b8,0x2a734a54,0x31a56af6,0x0c5d9160,0xaf83a19a,0x7fc9b41f,0xd079ef47,0xe3295281,0x5602e3e5,0xab915e69,0x225a1992,0xa387f6b2,0x7e981613,0xfc6cf59a,0xd34a7378,0xb608b7d6,0xa9eb93d9,0x26ddb218,0x65f33f5f,0xf9314442,0x5d5c0599,0xea72e774,0x1605a502,0xec6cbc9f,0x7f8a1bd1,0x4dd8cf07,0x2e6d79e0,0x6990418f,0xcf77bad9,0xd4fe0147,0xfef4a3e8,0x85c45bde,0xb58f8e67,0xa63eb8d7,0xc69bd19b,0xda442dca,0x3c0c1743,0xe6f39d49,0x33568804,0x85eb6320,0xda223445,0x36c4a941,0xa9185589,0x71b22d67,0xf59a2647,0x3c8b583e,0xd7717ded,0xdf05699c,0x4378367d,0x1c459339,0x85133b7f,0x49800ce2,0x3666ca0d,0xaf7ab504,0x4ff5b8f1,0xc23772e3,0x3544f31e,0x0f673a57,0xf40600e1,0x7e967417,0x15a26203,0x5f2e34ce,0x70c7921a,0xd1c190df,0x5bb5da6b,0x60979c75,0x4ea758a4,0x078fe359,0x1664639c,0xae14e73b,0x2070ff03};

    char* des = (char*)malloc(len);
    
    unsigned int *da = (unsigned int*)des;
    unsigned int *db = (unsigned int*)src;

    for(size_t i=0;i<len;i+=4)
    {
        int index = (i+(i/132))%132;
        da[i/4] = table[index]^db[i/4];
    }
    return (char*)da;
}
#include<stdlib.h>
void* MetadataLoader::LoadMetadataFile(const char* fileName)
{
    std::string resourcesDirectory = utils::PathUtils::Combine(Runtime::GetDataDir(), utils::StringView<char>("Metadata"));

    std::string resourceFilePath = utils::PathUtils::Combine(resourcesDirectory, utils::StringView<char>(fileName, strlen(fileName)));

    int error = 0;
    FileHandle* handle = File::Open(resourceFilePath, File::kFileModeOpen, File::kFileAccessRead, File::kFileShareRead, File::kFileOptionsNone, &error);
    if (error != 0)
        return NULL;
    size_t length = File::GetLength(handle, &error);
    if (error != 0)
    {
        return NULL;
    }
    void* fileBuffer = MemoryMappedFile::Map(handle);

    File::Close(handle, &error);
    if (error != 0)
    {
        MemoryMappedFile::Unmap(fileBuffer);
        fileBuffer = NULL;
        return NULL;
    }
    
    return (void*)decrypt_file((char*)fileBuffer,length);
}
