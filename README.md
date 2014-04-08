shaco-tool
=================
shaco-client-dump
=================
1. 下载google-breakpad
svn checkout http://google-breakpad.googlecode.com/svn/trunk/ google-breakpad

2. 拷贝google-breakpad到android应用的同级目录
3. 修改的andorid应用的Android.mk：
LOCAL_PATH := $(call my-dir)
这行改为
MY_ROOT_PATH := $(call my-dir)
include $(MY_ROOT_PATH)/../../../google-breakpad/android/google_breakpad/Android.mk
LOCAL_PATH := $(MY_ROOT_PATH)

LOCAL_C_INCLUDES 添加头文件包含目录：
     $(LOCAL_PATH)/../../../ \
     $(LOCAL_PATH)/../../../google-breakpad/src/common/android/include \
     $(LOCAL_PATH)/../../../google-breakpad/src
LOCAL_WHOLE_STATIC_LIBRARIES添加：
breakpad_client

4. 在cocos2dx应用中添加：
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
/* added to support googlebreakpad */
#include "google-breakpad/src/client/linux/handler/exception_handler.h"
#include "google-breakpad/src/client/linux/handler/minidump_descriptor.h"
google_breakpad::MinidumpDescriptor* DUMP_DESC = NULL;
google_breakpad::ExceptionHandler* DUMP_EH = NULL;
#endif

bool AppDelegate::applicationDidFinishLaunching()
{
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
    JniMethodInfo minfo;
    bool isHave = JniHelper::getStaticMethodInfo(minfo,"com/shengjoy/common/common","getSdcardPath", "()Ljava/lang/String;");
    if (isHave) {
        jstring jstr = (jstring)minfo.env->CallStaticObjectMethod(minfo.classID, minfo.methodID);
        char *path = (char*)minfo.env->GetStringUTFChars(jstr, 0);
        DUMP_DESC = new google_breakpad::MinidumpDescriptor(path);
        DUMP_EH = new google_breakpad::ExceptionHandler(*DUMP_DESC, NULL, NULL, NULL, true, -1);
    }
#endif
...
}
这样就会在sdcard根目录生成dmp文件

5. 查看dump文件
在linux下编译google-breakpad
./configure
make && make install

将dmp文件及对应的android目录obj目录下的so文件放到shaco-client-dump脚本同一目录下
运行shaco-client-dump
