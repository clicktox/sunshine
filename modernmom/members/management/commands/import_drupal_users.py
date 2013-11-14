from django.core.management.base import NoArgsCommand
from optparse import make_option
from urlparse import urlparse,urljoin
from django.conf import settings
from time import strftime
import urllib2
import re

from django.utils.safestring import mark_safe

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError: # django < 1.5
    from django.contrib.auth.models import User

from members.models import MemberSignature,Avatar,MemberAddress

from django.forms import EmailField
import MySQLdb
import urllib, urlparse, os, re, copy
from urllib import urlretrieve
from django.contrib.sites.models import Site
import hashlib,time, urllib2
import imghdr

from photologue.models import get_storage_path
from django.contrib.redirects.models import Redirect

import lxml, urllib2,datetime
from django.utils.timezone import make_aware,get_default_timezone
from django.utils.html import strip_tags
from django.template.defaultfilters import removetags

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
    )
    help = 'Update Category Article Counts'
    args = ''

    def handle_noargs(self, **options):
        site = Site.objects.get_current()

        sql = "SELECT dst, uuid, \
content_type_profile.field_first_name_value, \
content_type_profile.field_last_name_value,  \
content_type_profile.field_profile_about_value,  \
content_type_profile.field_profile_private_value,  \
content_type_profile.field_profile_gender_value,  \
content_type_profile.field_profile_dob_value,  \
users.uid, \
users.name, \
users.pass, \
users.mail, \
users.signature, \
users.created, \
users.access, \
users.login, \
users.status, \
users.picture, \
url_alias.dst \
FROM pressflow.content_type_profile \
inner join node on content_type_profile.nid = node.nid \
inner join users on users.uid = node.uid \
inner join  uuid_users on uuid_users.uid = users.uid \
left join url_alias on src = CONCAT('user/',users.uid) where users.created >= UNIX_TIMESTAMP(DATE_SUB(now(), INTERVAL 1 MONTH));"

        db = MySQLdb.connect(host="localhost", user="root", passwd="r00t!", db="pressflow") # name of the data base
        cur = db.cursor()
        cur.execute(sql)
        member_results =  cur.fetchall()       
        for row in member_results:
            try:
                slug = row[0].split('/')[1]
            except:
                slug = None
            uuid = row[1]
            first_name = row[2]
            last_name = row[3]
            about_me = row[4]
            is_private_profile = row[5]
            gender = row[6]
            dob = row[7]
            uid = row[8]
            username = row[9]
            password = row[10]
            email = row[11]
            signature = row[12]
            created = row[13]
            last_access = row[14]
            last_login = row[15]
            status = row[16]
            picture = row[17]
            dst = row[18]

            f = EmailField()
            try:
                email = f.clean(email)
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    try:
                        user = User.objects.create_user(username=username,email=email)
                    
                        user.date_joined = make_aware(datetime.datetime.fromtimestamp(float(created)),get_default_timezone())
                        user.last_login = make_aware(datetime.datetime.fromtimestamp(float(last_login)),get_default_timezone())
                        user.first_name=first_name
                        if not last_name is None:
                            user.last_name=last_name
                        if not int(status) == 1:
                            user.is_active = False
                        user.password = password      
                        try:
                            user.birthdate = make_aware(datetime.datetime.fromtimestamp(float(dob)),get_default_timezone())
                        except:
                            pass
                        user.save()
                    except:
                        user = None
                except Exception as ue:
                    user = None
                print user
                if (not user == None):
                    #handle the redirects...
                    old_path = '/%s' % dst
                    new_path = user.get_absolute_url()
                    redirect, c = Redirect.objects.get_or_create(site=site,old_path=old_path,new_path=new_path)
                
                    try:
                        about_me = removetags(about_me.decode('windows-1252'),'img font p div span')
                        signature = removetags(signature.decode('windows-1252'),'img font p div span')
                        signature = '%s %s' % (about_me,signature)
                        member_sig,c = MemberSignature.objects.get_or_create(member=user,defaults={'signature':signature})
                        member_sig.signature = signature
                        member_sig.save()
                    except:
                        pass
                    
                    """
                    In order to ensure we are not constantly downloading images ( get_storage_path assigns today as directory in format 2013_11_11 ), we need to use some date from the records
                    """
                    if not user.avatar:
                        if (not picture == ''):
                            try:
                                avatar_url = 'http://www.modernmom.com/%s' % picture
                                p =  '%d_%d_%d' % (user.date_joined.year,user.date_joined.month,user.date_joined.day)
                                thefilename = picture.split('/')[-1]
                                rp = os.path.join(settings.PHOTOLOGUE_DIR, p) #,picture.split('/')[-1])
                                ap = os.path.join(settings.MEDIA_ROOT,rp)
                                if not os.path.exists(ap):
                                    os.mkdir(ap)
                                rp = os.path.join(rp, thefilename)
                                ap = os.path.join(ap, thefilename)
                       
                                avatar = self.fetch_avatar(avatar_url,rp,ap)
                                user.avatar = avatar
                                user.save()
                            except Exception as image_e:
                                print 'Avatar Failed: %s' % image_e
            except Exception as e:
                print e
            """
            #member address
            try:
                location_query = 'SELECT location.name, location.street, location.additional, location.city, location.province, location.postal_code, location.country, \
                location.latitude, location.longitude, location.source, location.is_primary \
                FROM pressflow.location_instance \
                inner join node on node.nid = location_instance.nid \
                inner join users on users.uid = node.uid \
                inner join location on location_instance.lid = location.lid \
                where users.uid = %s;' % uid
                cur.execute(location_query)
                location_results =  cur.fetchall()       
                for location_row in location_results:
                    location_name,location_street,location_street2,location_city,location_state,location_postal,location_country,location_lat,location_long,location_source,location_is_primary = location_row
                    member_address,c = MemberAddress.objects.get_or_create(member=user,street=location_street,postal_code=location_postal,
                                                                         defaults={'additional':location_street2,'territory':location_state,'country':location_country,'latitude':location_lat,'longitude':location_long}) 
            except Exception as location_e:
                print 'Location Error: %s' % location_e                       
            """
    
    def fetch_avatar(self,image_url,relpath=None,outpath=None):
        if relpath is None:
            fi = hashlib.md5(str(time.time())).hexdigest()
            img = urllib2.urlopen(image_url).read()
            t = imghdr.what('ignore',img)
            if t is None:
                t = image_url.split('.')[-1]
            fi = '%s.%s' % (fi,t)
            relpath = get_storage_path(None,fi) #os.path.join('photologue/photos/','%s' % fi)
            outpath = os.path.join(getattr(settings, 'MEDIA_ROOT', None),relpath)
                
        if not os.path.exists(outpath):
             urlretrieve(image_url,outpath)
        try:
            photo,create = Avatar.objects.get_or_create(image=relpath)
        
        except Exception as e:
            print title
            print caption
            raw_input(e)
        return photo
    
    def old_fetch_avatar(self,image_url):
        fi = hashlib.md5(str(time.time())).hexdigest()
        img = urllib2.urlopen(image_url).read()
        t = imghdr.what('ignore',img)
        if t is None:
            t = image_url.split('.')[-1]
        fi = '%s.%s' % (fi,t)
        relpath = get_storage_path(None,fi) #os.path.join('photologue/photos/','%s' % fi)
        outpath = os.path.join(getattr(settings, 'MEDIA_ROOT', None),relpath)
        if not os.path.exists(outpath):
             urlretrieve(image_url,outpath)
        photo,create = Avatar.objects.get_or_create(image=relpath)
        return photo
