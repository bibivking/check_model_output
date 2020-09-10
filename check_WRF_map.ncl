;*******************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
;*******************************************

begin

; ================================= Predefine ==================================
; (time)
var_1D = (/ "HFX_FORCE","LH_FORCE","TSK_FORCE","HFX_FORCE_TEND",     \
            "LH_FORCE_TEND","TSK_FORCE_TEND", "T00", "P00", "TLP",   \
            "TISO", "TLP_STRAT","P_STRAT", "MAX_MSTFX", "MAX_MSTFY", \
            "SAVE_TOPO_FROM_REAL", "P_TOP" /)

; (Time, south_north, west_east)
var_3D = (/"Q2", "T2", "TH2", "PSFC", "U10", "V10", "LU_INDEX", "VAR_SSO",\
           "MU", "SWDOWN", "GLW", "SWNORM", "TAOD5502D", "OLR", "ALBEDO", \
           "ALBBCK", "EMISS", "NOAHRES", "TMN", "XLAND", "UST", "PBLH",   \
           "HFX", "QFX", "LH", "ACHFX", "ACLHF", "SNOWC", "SR", "REFD_MAX", \
           "PCB", "PC", "LANDMASK", "LAKEMASK", "SST", "SST_INPUT", "SHDMAX", \
           "SHDMIN", "SNOALB", "TPW", "LWP", "IWP", "CLWP", "RWP", "CIWP",\
           "FPWP", "MEAN_IVT_U", "MEAN_IVT_V", "FRZLVL", "COD2D_OUT", \
           "CTOP2D_OUT", "RAINC", "RAINSH", "RAINNC", "I_RAINC", "I_RAINNC",\
           "SNOWNC", "GRAUPELNC", "HAILNC", "SEAICE", "XICEM", "SFROFF", \
           "UDROFF", "IVGTYP", "ISLTYP", "VEGFRA", "GRDFLX", "ACGRDFLX", \
           "ACSNOM", "SNOW", "SNOWH", "CANWAT", "SSTSK", "COSZEN", "LAI",\
           "LISPOROSITY", "VAR", "F", "E", "SINALPHA", "COSALPHA", "HGT",\
           "TSK", "MUB", "COMDBZ", "RI_SEPA", "IT_SEPA", "CSI" /)

; (Time, 6, south_north, west_east)
var_4D_soil = (/ "TSLB", "SMOIS", "SH2O", "RAINNCV_SEPA", "RAINNC_SEPA"/)

; (Time, 29, south_north, west_east)
var_4D_29 = (/ "T", "P", "PB", "P_HYD", "QVAPOR", "QCLOUD", "QRAIN",\
               "QICE", "PHYS_TOT", "QSNOW", "REFC", "REFR", "REFI", \
               "REFS", "REFG", "REFH", "REFL_10CM", "CLDFRA" /)

; (Time, 29, south_north, west_east_stag)
var_4D_29_stag = (/ "U", "V" /)

; (Time, 30, south_north, west_east)
var_4D_30_stag = (/ "W","PH","PHB" /)


; =================================== Path =====================================
case_name = "Princeton_ctl_watmove_new_veg"
time_step = 248

; ============================== Read WRF file =================================
filename  = "/g/data/w35/mm3972/model/wrf/NUWRF/LISWRF_configs/"+case_name+"/WRF_output/wrfout_d01_2009-03-01_03:00:00"


f = addfile (filename,"r")

do var_num = 0, dimsizes(var_1D)-1
  print(f->$var_1D(var_num)$@description + ": "+ f->$var_1D(var_num)$(time_step-1))
end do


; ================================= Plotting ===================================
res                    = True
res@cnFillMode         = "RasterFill"            ; Raster Mode
res@cnFillOn           = True                            ;��ɫ
res@tmBorderThicknessF = 3.0

res@gsnDraw            = True  ; Don't draw plots
res@gsnFrame           = True  ; ����ҳ
res@lbLabelBarOn       = True

;************** ����labelbar ***************
res@lbBoxLinesOn       = True                       ;�ر�lbar box ����
res@lbTitleFont        = 25
res@lbLabelFont        = 25
res@lbTitleFontHeightF = 0.013
res@lbLabelFontHeightF = 0.013
res@txString      = ""
res@tmXBLabelFont      = 25 ;Sets the font index for the bottom X-Axis labels.
res@tmYLLabelFont      = 25

;*************** ���õ�ֵ�� *****************
res@cnLinesOn          = False                       ; �رյ�ֵ������
res@cnLineColor        = "black"
res@cnLineThicknessF   = 1.5
res@cnLineLabelsOn     = False
res@gsnMaximize        = True
res@cnExplicitLabelBarLabelsOn = True   ;?
res@cnLevelSelectionMode = "ExplicitLevels"

;************ ����������ֵ��Χ **************
res@tmXBLabelFontThicknessF = 0.015
res@tmYLLabelFontThicknessF = 0.015
res@tmXBLabelFontHeightF = 0.015
res@tmYLLabelFontHeightF = 0.015
res@tmYLMode  = "Explicit"
res@tmXBMode  = "Explicit"
res@gsnLeftString = ""
res@gsnRightString = ""


; ================================= Plotting ===================================
pic = "./plots/Check_"+case_name+"_ts-"+time_step
wks = gsn_open_wks("pdf",pic)
gsn_define_colormap(wks,"rainbow") ;"ViBlGrWhYeOrRe") ;"BlueYellowRed")   "amwg") ;

do var_num = 0, dimsizes(var_3D)-1
  print(f->$var_3D(var_num)$@description)
  res@tiMainString = f->$var_3D(var_num)$@description
  plot = gsn_csm_contour(wks,f->$var_3D(var_num)$(time_step-1,:,:),res)
end do

do var_num = 0, dimsizes(var_4D_soil)-1
  print(f->$var_4D_soil(var_num)$@description)
  res@tiMainString = f->$var_4D_soil(var_num)$@description
  plot = gsn_csm_contour(wks,f->$var_4D_soil(var_num)$(time_step-1,0,:,:),res)
end do

do var_num = 0, dimsizes(var_4D_29)-1
  print(f->$var_4D_29(var_num)$@description)
  res@tiMainString = f->$var_4D_29(var_num)$@description
  plot = gsn_csm_contour(wks,f->$var_4D_29(var_num)$(time_step-1,0,:,:),res)
end do

do var_num = 0, dimsizes(var_4D_29_stag)-1
  print(f->$var_4D_29_stag(var_num)$@description)
  res@tiMainString = f->$var_4D_29_stag(var_num)$@description
  plot = gsn_csm_contour(wks,f->$var_4D_29_stag(var_num)$(time_step-1,0,:,:),res)
end do

do var_num = 0, dimsizes(var_4D_30_stag)-1
  print(f->$var_4D_30_stag(var_num)$@description)
  res@tiMainString = f->$var_4D_30_stag(var_num)$@description
  plot = gsn_csm_contour(wks,f->$var_4D_30_stag(var_num)$(time_step-1,0,:,:),res)
end do

end
