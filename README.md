# teekopolis-yum-repo

Packaging for my favorite packages. I take security seriously, so all of these packages will be compiled with hardened
`CFLAGS` and `LDFLAGS` and the like.

## Update Flow

There are four steps to building and deploying the repository.

 1. `make download` syncs the remote S3 repository down to `build/repo`.
 1. `make`: does the following:
   1. `make fetch_sources`: Fetch source tarballs for the spec files.
   1. `make build_srpms`: Build source RPMs from the spec files and the downloaded sources into `build/source`.
   1. `make build_rpms`: Build RPMs for each architecture and OS release. As of now, `fedora-23-i386` and
      `fedora-23-x86_64`.
   1. `make prune_repo`: Delete old versions of packages from `build/repo`.
   1. `make deploy_repo`: Deploy new packages into `build/repo`.
   1. `make gen_repo_metadata`: Generate repo metadata.
 1. `make sign`: does the following:
   1. `make sign_rpms`: Sign the built rpms in `build/repo` with GPG.
   1. `make gen_repo_metadata`: Generate repo metadata.
 1. `make upload` simply syncs the contents of `build/repo` with the S3 bucket.

Therefore, to build a complete working repository, all that is required is:

```
$ make download
$ make
$ make sign
$ make upload
```

The signing step can be skipped if you don't care about security. But seriously, don't do that. Sign your RPMs, you're
an _adult_.

If you're not planning on using S3 or hosting your repository, you can skip the `make download` and `make upload` steps.

## Environment Variables

There are a few environment variables used by the `Makefile` that you should have defined and exported:

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>AWS_ACCESS_KEY_ID</code></td>
            <td>Your AWS access key id for S3 access.</td>
        </tr>
        <tr>
            <td><code>AWS_SECRET_ACCESS_KEY</code></td>
            <td>Your AWS secret access key for S3 access.</td>
        </tr>
        <tr>
            <td><code>S3_BUCKET</code></td>
            <td>The name of your S3 bucket.</td>
        </tr>
        <tr>
            <td><code>GPG_KEY_ID</code></td>
            <td>The GPG key id to use to sign the packages.</td>
        </tr>
    </tbody>
</table>

## AWS IAM Credentials

The AWS IAM user you use must have the following effective policy:

```
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "s3:ListBucket",
            "s3:GetBucketLocation"
         ],
         "Resource":"arn:aws:s3:::{{ bucket_name }}"
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:PutObject",
            "s3:GetObject",
            "s3:DeleteObject"
         ],
         "Resource":"arn:aws:s3:::{{ bucket_name }}/*"
      }
   ]
}
```

Your bucket must also have the following effective policy for your machines to be able to access it publicly over the
internet:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{{ bucket_name }}/*"
        }
    ]
}
```

## Security

Things to fix:

 - [ ] MakeMKV binaries and libraries are in bad shape, security-wise.
 - [ ] StepMania is statically linked to its dependencies, we can only await an upstream solution where the source code
       is updated to use modern libraries.
 - [ ] StepMania's GTK 2 loading screen doesn't have a stack canary; somehow it's getting compiled without a stack
       protector.

Everything else fully passes the `checksec --file` test, returning the following:

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   /usr/bin/ffmpeg
```

## To Do

 - [ ] Test and verify package signing.
 - [ ] Package VLC.
 - [ ] Package GStreamer plugins:
    * `gstreamer-plugins-bad`
    * `gstreamer-plugins-ugly`
    * `gstreamer-plugins-libav`

# Credits

Thanks to [Simone Caronni](http://negativo17.org/handbrake/) for much of the inspiration and work done on packaging
things.
