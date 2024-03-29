; FILE: anomalies.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
begin

wkdir = getenv("WKDIR")
variab_dir = getenv("variab_dir")
casename = getenv("CASENAME")
yr1 = getenv("FIRSTYR")
yr2 = getenv("LASTYR")

firstyr = stringtointeger(yr1)
lastyr = stringtointeger(yr2)
nyrs = lastyr-firstyr+1
nmons = nyrs*12

time_coord = getenv("time_coord")
lat_coord = getenv("lat_coord")
lon_coord = getenv("lon_coord")
lev_coord = getenv("lev_coord")


lat_var = getenv("lat_var")
lon_var = getenv("lon_var")
hyam_var = getenv("hyam_var")
hybm_var = getenv("hybm_var")
time_var = getenv("time_var")

file_path = getenv("DATADIR")

zg_var = getenv("zg_var")
ps_var = getenv("ps_var")

; Z500 
if( fileexists(variab_dir+"/EOF_500hPa/model/netCDF/"+casename+".Z500.ANOMS.nc") ) then

print(variab_dir+"/netCDF/"+casename+".Z500.ANOMS.nc exists!!")

else

f_zg = addfile(file_path+"/mon/"+casename+"."+zg_var+".mon.nc","r")
f_ps = addfile(file_path+"/mon/"+casename+"."+ps_var+".mon.nc","r")

time = f_zg->$time_var$
lat = f_zg->$lat_var$
lon = f_zg->$lon_var$
nlat = dimsizes(lat)
nlon = dimsizes(lon)
hyam = f_zg->$hyam_var$
hybm = f_zg->$hybm_var$

slat = new((/nlat+1/),"double")
gw = new((/nlat/),"double")
gw!0 = lat_coord
gw&$lat_coord$ = lat
slat(0) = -90.d0
slat(nlat) = 90.d0
do i=1,nlat-1
 slat(i) = (lat(i-1)+lat(i))/2.d0
end do
pi = 4.d0*atan(1.d0)
do i=0,nlat-1
 gw(i) = sin(slat(i+1)/180.d0*pi)-sin(slat(i)/180.d0*pi)
end do

time_all = f_zg->$time_var$
date_all = ut_calendar(time_all,-2)
year_all = date_all/10000

start_date = firstyr*10000+201
end_date = (lastyr+1)*10000+101

do i=0,dimsizes(date_all)-1
   if( date_all(i).eq.start_date ) then
      i1 = i
   end if
   if( date_all(i).eq.end_date ) then
      i2 = i
   end if
end do

win_anom = new ((/nyrs-1,nlat,nlon/),"float")
win_anom!0 = "year"
win_anom&year = ispan(firstyr+1,lastyr,1) 
win_anom!1 = lat_coord
win_anom&$lat_coord$ = lat
win_anom!2 = lon_coord
win_anom&$lon_coord$ = lon
win_anom@long_name = "Winter (DJFM) 500mb height anomaly"
win_anom@units = "meters"


z = f_zg->$zg_var$($time_coord$|i1:i2,$lev_coord$|:,$lat_coord$|:,$lon_coord$|:)
ps = f_ps->$ps_var$($time_coord$|i1:i2,$lat_coord$|:,$lon_coord$|:)
z500 = vinth2p(z,hyam,hybm,500.,ps,2,1000.,1,False) ; (time,plev,lat,lon)
delete (z)
delete (ps)
anom = (/rmMonAnnCycTLL(z500(:,0,:,:))/)
delete (z500)
n = 11
do yr = firstyr+1,lastyr
  win_anom(yr-firstyr-1,:,:) = (/(anom(n,:,:)+anom(n+1,:,:)+anom(n+2,:,:)+anom(n+3,:,:))/4./)
  n = n + 12
end do
fo = addfile(variab_dir+"/EOF_500hPa/model/netCDF/"+casename+".Z500.ANOMS.nc","c")
fo->Z500_ANOM = win_anom
fo->gw = gw

delete(f_ps)
delete(f_zg)
delete(win_anom)

end if


end
