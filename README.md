# docker-doug
DOUG - DOcker Update Guard ([Documentation](https://shaded-enmity.github.io/docker-doug/))

## What it is?
First and foremost, the project is split into a CLI and a library. The CLI
portion of the code is a working example of how to use the library and also
hosts several interesting features that we'll outline below.

## How to get it?

Install `libdoug` via `pip`, the CLI is bundled in:

```bash
$ pip install libdoug
```

## What is included?

### doug-cli

Basic usage for the CLI:

```bash
$ doug-cli --help
usage: doug-cli [-h] [-f] [-u USER] [-p PASSWORD] [-e EMAIL] [-r REGISTRY]
                   [-a BASEAUTH] [-n]
                   {dump-local,dump-remote,docker-cli,dependencies,update} ...

doug-cli libdoug interface

positional arguments:
  {dump-local,dump-remote,docker-cli,dependencies,update}
                        sub-command help
    dump-local          Dump locally present tags
    dump-remote         Dump remotely present tags
    docker-cli          Parse Dockers CLI
    dependencies        Visualize dependencies of target Image
    update              Update Local/Remote tags

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Do not ask for confirmations
  -u USER, --user USER  Username for the Hub
  -p PASSWORD, --password PASSWORD
                        Password for the Hub
  -e EMAIL, --email EMAIL
                        Email for the Hub
  -r REGISTRY, --registry REGISTRY
                        Registry URL we target
  -a BASEAUTH, --baseauth BASEAUTH
                        HTTP Basic Auth string
  -n, --no-push         Do not push local changes upstream
``` 

Examples:
```bash
$ doug-cli dependencies fedora:21
Dependency Walker:
╺┬834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89 [u'fedora:21', u'fedora:latest']
 └┬cdbaf1c8a5622728a9ec6502f049ec64b245ad69a3f0436e9c92c051c83ef275 
  ├─654d2ca2aaa2f1244ea40d8290883c5964a7f971f778e230414b7830e3829867 [u'pavelo/doug:1.0.3-1']
  ├─d65423a7581095bf05573180e0f0fab4566d888ebb1cb64a85d33ded02cc0607 [u'pavelo/doug:1.0.2']
  ├─d52aadb426e73771f5545d7e0810733d19e5a5904a26ae1e7435ccb8a7a17b95 [u'pavelo/doug:1.0.0', u'pavelo/doug:1.0.1']
  └─6896ae86f1a1115c028111994efcd617d08ad90eecaf5d1dc2deffcd6d4de5a4 [u'pavelo/doug:latest', u'pavelo/doug:1.0.3']

$ doug-cli docker-cli -- docker run -it --rm -p 3000:3000 -v /:/volume -v /another:/some/place/else -e A=B -e B=C myImage /bin/bash -c "echo Test!"
Flags:    -i / --interactive = True
	  -t / --tty = True
	  --rm = True
	  -p / --publish = 3000:3000
	  -v / --volume = /:/volume
	  -v / --volume = /another:/some/place/else
	  -e / --env = A=B
	  -e / --env = B=C
Verb:     run
Context:  ['myImage', '/bin/bash', '-c', 'echo Test!']
Workdir:  /home/podvody/Repos/docker-doug

$ doug-cli dump-local fedora
Local tags:
  20 : 6cece30db4f924da43969a12fdf47492ada22b372a0968d6ca8b71d25876629f
  21 : 834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89
  heisenbug : 6cece30db4f924da43969a12fdf47492ada22b372a0968d6ca8b71d25876629f
  latest : 834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89
  rawhide : aecd12627ded593a207e32e3537661d1fae1cdc8e0f2e074aa4a730213e5a953

$ doug-cli dump-remote fedora
Remote tags:
  20 : 6cece30db4f924da43969a12fdf47492ada22b372a0968d6ca8b71d25876629f
  21 : 834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89
  heisenbug : 6cece30db4f924da43969a12fdf47492ada22b372a0968d6ca8b71d25876629f
  latest : 834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89
  rawhide : aecd12627ded593a207e32e3537661d1fae1cdc8e0f2e074aa4a730213e5a953

$ doug-cli update fedora
Local and Remote are up to date!

$ docker rmi fedora:latest
Untagged: fedora:latest

$ doug-cli update fedora
Local and Remote Diffs:
  R latest : 834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89
Resolve conflicts [y/n]? [y] y
Resolutions: 
  ┍ docker tag 834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89 fedora:latest
  ╰╼ done! 
```


### libdoug

Let's summarize what is included by default and some future aims for the `libdoug`:

* Hub/Registry
  * Get API `token` from Hub upon authenticating
  * `Token` cached for 2 hours
  * Also gives `ro` access for public registries
  * Public registries are hidden behind special user `stackbrew`
  * Fetch all tags in a repository

* Updates
  * Handle local/remote updates to a repository
  * Repo diffs, Image trees, Conflict solvers ...
    * Version-Release conflict solver
      * Works kinda like RPMs
      * Push/Pull the highest version, remove the rest

* Docker API and diagnostics tools
  * Got a 4 line long docker command trying to figure out what it does?
    * or need a sensible format for logging? See the example of `docker-cli` sub-command above
  * Programmatic definitions of the following Docker APIs: CLI, Docker socket v.1.16, Registry, Hub
    * Autogenerated with (and manually fine-tuned): [docker-devour](https://github.com/shaded-enmity/docker-devour)
  * The `dependencies` sub-command can be used for visualizing deeply nested hierarchies of images

* What's in the works
  * Toolchain for propagation of information about updates in the infrastructure
    * When a new `Version-Release` tag appers in the remote, we should rebase all local children on top of the new one 
    * That means editing `Dockerfile`'s and issuing `build` requests
    * Or editing of `k8s` pod `YAML`s
  * Documentation


