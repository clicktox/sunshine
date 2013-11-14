

from django.core.management.base import NoArgsCommand
from optparse import make_option
from urlparse import urlparse,urljoin
from django.conf import settings
from datetime import datetime, timedelta
from time import strftime
import urllib2
import re

from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from members.models import *
from django.forms import EmailField
import MySQLdb

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
    )
    help = 'Update Category Article Counts'
    args = ''

    def handle_noargs(self, **options):
        
        sql = "SELECT \
        users.uid,users.mail, \
        location.street, \
        location.additional, \
        location.city, \
        location.province, \
        location.postal_code, \
        location.country, \
        location.latitude, \
        location.longitude, \
        field_insider_dob_value, \
        uuid_users.uuid \
        FROM `pressflow`.`content_type_insider_profile` as profile \
        inner join node on node.nid = profile.nid \
        inner join users on users.uid = node.uid \
        inner join uuid_users on uuid_users.uid = users.uid \
        left join location on profile.field_insider_mailing_address_lid = location.lid;"

        db = MySQLdb.connect(host="localhost", user="root", passwd="r00t!", db="pressflow") # name of the data base
        cur = db.cursor()
        cur.execute(sql)
        fo_errors = open('import_insiders_errors','w')
        for row in cur.fetchall() :
            uid = row[0]
            email = row[1]
            street = row[2]
            additional = row[3]
            city = row[4]
            province = row[5]
            postal_code = row[6]
            country = row[7]
            latitide = row[8]
            longitude = row[9]
            dob = row[10]
            uuid = row[11]

            f = EmailField()
            try:
                email = f.clean(email)
                try:
                    user = User.objects.get(email=email)
                    try:
                        member = Member.objects.get(user=user)
                        insider,c = Insider.objects.get_or_create(user=user)
                        try:
                            try:
                                address = member.memberaddress
                            except MemberAddress.DoesNotExist:
                                address = MemberAddress(member=member)
                            address.street = street
                            address.additional = additional
                            address.city = city
                            address.territory = province
                            address.postal_code = postal_code
                            address.country = country
                            address.latitide  = latitide
                            address.longitude = longitude
                            address.save()
                        except Exception as e:
                            print ('Error saving address %s' % e)
       
                    except Member.DoesNotExist:
                        print('Member object not found %s' % uid)
                except User.DoesNotExist:
                    print('Could not find %s' % email)  
                
               
                    
                
            except Exception as e:
                print e
                
            """
            for user in users:
                try:
                    print user.get_profile()
                except MemberProfile.DoesNotExist:
                    print 'Error for %s' % user.username
                    mp = MemberProfile(user=user)
                    mp.save()
            """
    def fetch_avatar(image_url):
        fi = hashlib.md5(str(time.time())).hexdigest()
        if img is None:
            img = urllib2.urlopen(image_url).read()
        t = imghdr.what('ignore',img)
        if t is None:
            return None
        fi = '%s.%s' % (fi,t)
        fi = os.path.join(getattr(settings, 'IMAGEKIT_AVATAR_PATH', None),fi)
        relpath = fi
        outpath = os.path.join(getattr(settings, 'MEDIA_ROOT', None),relpath)
        desc = title
        if not os.path.exists(outpath):
            print 'Fetching %s' % image_url
            urlretrieve(image_url,outpath)
        photo,create = ItemImage.objects.get_or_create(image=relpath,defaults={'title':title,'source':None,'url':image_url })
        return photo
