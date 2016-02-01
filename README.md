# teekopolis-yum-repo

Packaging for my favorite packages. I take security seriously, so all of these packages will be compiled with hardened
`CFLAGS` and `LDFLAGS` and the like.

## Security

Things to fix:

 - [ ] LAME binary has an RPATH.
 - [ ] MakeMKV binaries and libraries are in bad shape.

Good:

 - [x] <s>ffmpeg binaries and libraries</s>
 - [x] <s>HandBrake CLI and GTK</s>
 - [x] <s>libaacplus</s>
 - [x] <s>libdvdcss</s>
 - [x] <s>libfdk-aac</s>
 - [x] <s>libmp3lame</s>
 - [x] <s>libmfx</s>
 - [x] <s>libvo-aacenc</s>
 - [x] <s>libvo-amrwbenc</s>
 - [x] <s>libxvidcore</s>
 - [x] <s>x264 binary and library</s>
 - [x] <s>x265 binary and library</s>

## To Do

 - [ ] Automate downloading of sources and stuff.
    * ffmpeg
    * handbrake
    * libmfx
    * makemkv
    * x264
 - [ ] Cross-compile x265 for 8, 10, and 12-bit encoding ([example][x265-xcompile]).

 [x265-xcompile]: https://bitbucket.org/multicoreware/x265/src/dc62b47dd0d98f732165345883edac55320baec1/build/linux/multilib.sh?at=default&fileviewer=file-view-default
