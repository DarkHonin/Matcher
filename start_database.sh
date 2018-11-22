if [ ! -f db ]; then
    mkdir db
fi

mongod -dbpath db