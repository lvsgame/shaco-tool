import sys
import string

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s js"%(sys.argv[0])
        exit(1)

    fi = open(sys.argv[1], "r")
    c = fi.read()
    fi.close()

    fo = open("%s.out"%sys.argv[1], "w")
    c = c.replace('\r\n', '')
    c = c.replace('\n', '')
    fo.write(c)
    fo.close()
