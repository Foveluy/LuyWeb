import time


wd_ary = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
mon_ary = ['','Jan', 'Feb', 'Mar', 'Apr', 'May',
           'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def gmtime():
    '''
    a little bit faster way to get GMT time
    7% faster than standard lib
    '''
    metadata = time.gmtime()
    return '%s, %d %s %d %02d:%02d:%02d GMT' % (
        wd_ary[metadata.tm_wday],
        metadata.tm_mday,
        mon_ary[metadata.tm_mon],
        metadata.tm_year,
        metadata.tm_hour,
        metadata.tm_min,
        metadata.tm_sec)
