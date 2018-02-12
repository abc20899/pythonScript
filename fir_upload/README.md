**python脚本上传apk file到fir平台**

#### use:
* 首先配置好python3环境
* 下载脚本拷贝至项目的根目录
* 配置项目app module下的build.gradle文件,添加如下配置：
  
  ```
	//上传fir任务
	task firUpload {
		dependsOn 'assembleRelease'
		doLast {
		    def apkpath = ""
		    def bundleid = ""
		    android.applicationVariants.all { variant ->
		        variant.outputs.each { output ->
		            def outputFile = output.outputFile
		            if (outputFile != null && outputFile.name.endsWith('.apk')) {
		                if (variant.buildType.name == "release") {
		                    apkpath = outputFile
		                    bundleid = variant.applicationId
		                }
		            }
		        }
		    }
		    def appname = rootProject.ext.APP_NAME.replace("\"", "")
		    def verName = project.android.defaultConfig.versionName
		    def buildnum = project.android.defaultConfig.versionCode
		    def iconpath = getBuildDir().parent + "/src/main/res/mipmap-xxhdpi/ic_launcher.png"
		    def apitoken = "your fir apitoken"
		    //调用python脚本  这个脚本需要放在工程目录下
		    def process = """python3 upload_apk_fir.py ${appname} ${verName} ${buildnum} ${iconpath} ${
		        apkpath} ${bundleid} ${apitoken}""".execute()
		    //将python代码里面打印的内容在gradle窗口中打印出来
		    ByteArrayOutputStream result = new ByteArrayOutputStream()
		    def inputStream = process.getInputStream()
		    byte[] buffer = new byte[1024]
		    int length
		    while ((length = inputStream.read(buffer)) != -1) {
		        result.write(buffer, 0, length)
		    }
		    println(result.toString("UTF-8"))
			}
	}
	
	//./gradlew myBuild
	task myBuild() {
		dependsOn firUpload
	}
  ```
  其中 apitoken 设置成自己的fir apitoken
* 最后执行

	```
	//编译上传 预先配置好自动签名项
	./gradlew myBuild
	```