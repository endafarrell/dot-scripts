BACKUP_ROOT="/Users/efarrell/Dropbox"
if [ ! -d "$BACKUP_ROOT/dot.ssh" ]; then
	mkdir "$BACKUP_ROOT/dot.ssh"
fi
if [ ! -d "$BACKUP_ROOT/bin" ]; then
	mkdir "$BACKUP_ROOT/bin"
fi
cp -R /Users/efarrell/.ssh/* $BACKUP_ROOT/dot.ssh/
cp -R /Users/efarrell/bin/* $BACKUP_ROOT/bin/
