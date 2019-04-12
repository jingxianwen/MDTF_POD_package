#============================================================
# execute_ncl_calculate - call a nclPlotFile via subprocess call
#============================================================
def execute_ncl_calculate(nclPlotFile):
   """generate_plots_call - call a nclPlotFile via subprocess call

   Arguments:
   nclPlotFile (string) - full path to ncl plotting file name
   """
   import subprocess
   # check if the nclPlotFile exists -
   # don't exit if it does not exists just print a warning.
   try:
      pipe = subprocess.Popen(['ncl {0}'.format(nclPlotFile)], shell=True, stdout=subprocess.PIPE)
      output = pipe.communicate()[0]
      print('NCL routine {0} \n {1}'.format(nclPlotFile,output))
      while pipe.poll() is None:
         time.sleep(0.5)
   except OSError as e:
      print('WARNING',e.errno,e.strerror)

   return 0

#============================================================
# create html
#============================================================
def create_html(model):
   '''
   ----------------------------------------------------------------------
   Note
       create html of QTS figures
   ----------------------------------------------------------------------
   '''
   import os
   from post_process import execute_ncl_calculate

   print(model+": creating html ...")
   html=os.environ["HTMDIR"]+"template.html"
   html2=os.environ["QTSDIR"]+"transport_onto_TS.html"
   if os.path.isfile(html):
      fp = file(html)
      lines = fp.readlines()
      head = lines[0:45]
      partA= lines[45:61]
      tail = lines[61:85]
      partB= lines[85:97]
      fp.close()
      fp2= file(html2, 'w')
      cnt = 45
#      print model
      for i in partA:
         i=i.replace("CanESM2",model)
         head.insert(cnt, i)
         cnt = cnt +1
      cnt = 24
#      print model
      for i in partB:
         i=i.replace("CanESM2",model)
         tail.insert(cnt, i)
         cnt = cnt +1
      s = ''.join(head+tail)
      fp2.write(s)
      fp2.close()
#============================================================
# convert pdf to png
#============================================================
def convert_pdf2png():
    '''
    ----------------------------------------------------------------------
    Note
        convert pdf figures to png format
    ----------------------------------------------------------------------
    '''
    import os

    print("Converting *.pdf to *.png ...")
    if os.environ["CLEAN"] == "1":
       os.system("rm -rf "+os.environ["OUTDIR"])
       os.system("rm -rf "+os.environ["FIGDIR"])

    files = os.listdir(os.environ["FIGDIR"])
    a = 0
    while a < len(files):
       file1 = os.environ["FIGDIR"]+files[a]
       if file1[-3:] == ".png":
          a = a + 1
          continue
       file2 = os.environ["PNGDIR"]+files[a]
       os.system("pdfcrop --margins '5 5 5 5' "+file1+" "+file2+"; convert -density 400 "+file2+" -quality 100 "+file2[:-4]+".png")
       a = a+1
    os.system("\rm -f "+os.environ["FIGDIR"]+"*.*")
    os.system("\mv "+os.environ["PNGDIR"]+"*.pdf "+os.environ["FIGDIR"])
#    os.system("\mv "+os.environ["PNGDIR"]+"*.png "+os.environ["FIGDIR"])

#============================================================
# convert pdf to png for obs/reference
#============================================================
def convert_pdf2png_obs():
    '''
    ----------------------------------------------------------------------
    Note
        convert pdf figures to png format
    ----------------------------------------------------------------------
    '''
    import os
    print("Converting pdf to png ...")
    files = os.listdir(os.environ["FIGREF"])
    print(files)
    a = 0
    while a < len(files):
       file1 = os.environ["FIGREF"]+files[a]
       if file1[-3:] == ".png":
          a = a + 1
          continue
       file2 = os.environ["PNGREF"]+files[a]
       os.system("pdfcrop --margins '5 5 5 5' "+file1+" "+file2+"; convert -density 400 "+file2+" -quality 100 "+file2[:-4]+".png")
       a = a+1
    os.system("rm -f "+os.environ["FIGREF"]+"*.*")
    os.system("\mv "+os.environ["PNGREF"]+"*.pdf "+os.environ["FIGREF"])
#    os.system("\mv "+os.environ["PNGREF"]+"*.png "+os.environ["FIGREF"])

#============================================================
# move monthly and yearly files to mon_yr/
#============================================================
def mv_mon_yr(model):
    '''
    ----------------------------------------------------------------------
    Note
        mv *.mon.nc *.yr.nc to mon_yr/
    ----------------------------------------------------------------------
    '''
    import os
    import glob
    print(model+": mv *.mon.nc *.yr.nc to mon_yr/ ...")
    if len(glob.glob(os.environ["OUTDIR"]+model+".*.mon.nc"))>0:
       print("mv monthly files to "+os.environ["TMPDIR"]+"mon_yr/")
       os.system("mv "+os.environ["OUTDIR"]+model+".*.mon.nc "+os.environ["TMPDIR"])

    if len(glob.glob(os.environ["OUTDIR"]+model+".*.yr.nc"))>0:
       print("mv yearly files to "+os.environ["OUTDIR"]+"mon_yr/")
       os.system("\mv "+os.environ["OUTDIR"]+model+".*.yr.nc "+os.environ["TMPDIR"])    
