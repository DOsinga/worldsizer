<cfsetting showdebugoutput="no">
<!doctype html>
<html><!-- InstanceBegin template="/Templates/wfbook_template.dwt.cfm" codeOutsideHTMLIsLocked="false" --><head>
<meta charset="utf-8" />
<!-- InstanceBeginEditable name="title" -->
<title>CIA - The World Factbook</title>
<script type="text/javascript" language="javascript" src="audio/niftyplayer.js"></script>

<!-- InstanceEndEditable -->

<cfset whatever = "../">
<cfinclude template="../connections/GlobalVariables.cfm">
<cfinclude template="../connections/PubYearSetter.cfm">
<cfinclude template="../connections/udfs.cfm">
<cfinclude template="../includes/print.cfm">

  <cfset whatever = "../"> 
  <link href="../css/fullscreen-external.css" rel="stylesheet" type="text/css">
  <script src="../js/modernizr-latest.js"></script><!--developers version - switch to specific production http://modernizr.com/download/--> 
  <script type="text/javascript" src="../js/jquery-1.8.3.min.js"></script>
  <cfif isDefined("URL.staticOut")>
  	<script type="text/javascript" src="../js/jquery.main.js"></script>
</cfif>
  
  <!--- wfb styles --->
  <link rel="stylesheet" type="text/css" href="../styles/jquery.ui.core.css">
  <link rel="stylesheet" type="text/css" href="../styles/jquery.qtip.css">
  <link rel="stylesheet" type="text/css" href="../styles/listnav.css"/> 
  <link rel="stylesheet" type="text/css" href="../styles/navigation.css">
  <link rel="stylesheet" type="text/css" href="../styles/wfb_styles.css">
  <link rel="stylesheet" type="text/css" href="../scripts/galleria/themes/classic/galleria.classic.css">

  <script type="text/javascript" src="../scripts/wfb_scripts.js" charset="utf-8"></script>
  <script type="text/javascript" src="../scripts/jquery.idTabs.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="../scripts/jquery.listmenu.js"></script>
  <script type="text/javascript" src="../scripts/jquery.listnav.pack.2.1.js" charset="utf-8"></script>

  <script src="../scripts/jquery-ui-1.9.2.custom.js" type="text/javascript"></script>
  <script type="text/javascript" src="../scripts/jquery.qtip-2.0.js"></script>
  <script type="text/javascript" src="../scripts/jquery.qtip.min.js"></script>
  <script src="../scripts/imgscale.js"></script>
 <script src="../scripts/galleria/galleria-1.2.9.min.js"></script>

<!-- Internet Explorer CSS Fixes -->
<!--[if lt IE 7]> 
        <style type="text/css" media="all">@import url(<cfoutput>#whatever#</cfoutput>styles/IEFixes.css);</style>
    <![endif]-->
<!-- Disable IE6 image toolbar -->
<meta http-equiv="imagetoolbar" content="no" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script language="JavaScript" type="text/javascript">
		function clearSearch(myForm) {if (myForm.defaultValue==myForm.value) myForm.value = "";}
		function showSearch(myForm) {if (myForm.value=="") myForm.value = myForm.defaultValue;} 
		function MM_swapImgRestore() { //v3.0
		  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
		}
		function MM_preloadImages() { //v3.0
		  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
			var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
			if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
		} 
		 
		function MM_findObj(n, d) { //v4.01
		  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
			d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
		  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
		  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
		  if(!x && d.getElementById) x=d.getElementById(n); return x;
		}
		 
		function MM_swapImage() { //v3.0
		  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
		   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
		}
		
</script>

<!-- InstanceBeginEditable name="scripts" -->



<!-- InstanceEndEditable -->

<style type="text/css">
<!--
html, body {
     height: 100%;
}


body {
     background-color: #EEEEEE;
     background-image: url(../graphics/background_top.jpg);
     background-repeat: repeat-x;
}

#right_shadow {
     background-image:url(../graphics/right_shadow.jpg);
     background-repeat:repeat-y;
     background-position:top;
     color: #909;
}

#right_shadow_top {
     background-image:url(../graphics/right_shadow_top.jpg);
     background-repeat: repeat-y;
     background-position:top left;
}

#left_shadow {
     background-image:url(../graphics/left_shadow.jpg);
     background-repeat:repeat-y;
     background-position: top;
}

#left_shadow_top {
     background-image:url(../graphics/left_shadow_top.jpg);
     background-repeat: repeat-y;
     background-position: top right;
}

.title {
     font-size: 15px;
     font-weight: bold;
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-variant: small-caps;
     line-height: 15px;
     padding-left: 5px;
}

<!---.header {
     font-family: Arial, Helvetica, sans-serif;
     font-weight: bold;
     font-size: 11px;
     border-top-width: thin;
     border-top-style: solid;
     border-top-color: #666666;
     margin-top: 5px;
}--->

.intro {
     font-family: Arial, Helvetica, sans-serif;
     font-size: 11px;
     padding: 10px 0px 10px 5px;
     letter-spacing: .02em;
     line-height: 16px;
     text-align: left;
}

.whats-new-text {
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size: 10px;
     padding: 3px 5px 3px 5px;
     letter-spacing: 0.01em;
}

.wf-cover-text {
     font-size: 11px;
     font-family: Arial, Helvetica, sans-serif;
     color: #666666;
     letter-spacing: 0.01em;
     padding: 7px 5px 10px 10px;
}

.classification {
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size: 10px;
     font-weight: bold;
     color: #7F7F7F;
     vertical-align: middle;
     line-height: 22px;
     letter-spacing: 3px;
}
-->
</style>
</head>
<body style="background-color: #EEEEEE; margin: 0px;" class="yui-skin-sam">
<table border="0" align="center" cellpadding="0" cellspacing="0" style="height: 100%;">
	<tr>
		<td width="25" id="left_shadow_top">&nbsp;</td>
		<td height="35" align="center" class="classification">UNCLASSIFIED</td>
		<td width="25" id="right_shadow_top">&nbsp;</td>
	</tr>
	<tr>
		<td width="25" id="left_shadow">&nbsp;</td> 
		<td valign="top" bgcolor="#FFFFFF" style="padding: 10px 10px 0px 10px; width: 800px; height: 100%;">
			<table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
				<tr>
							<td><cfinclude template="../includes/banner.cfm"></td> 
						</tr>
						<tr>
							<td align="right" style="padding-top: 5px; padding-bottom: 10px; background-image:url(../graphics/country_gradiant_back.jpg); background-position: top; background-repeat: repeat-x;"><cfinclude template="../includes/country_list.cfm">
							</td>
						</tr>
						<tr>
							<td><cfinclude template="../includes/wfb_navigation.cfm"></td>
						</tr>
						<tr> 
							<td style="height: 100%;">
								<!-- InstanceBeginEditable name="mainContent" -->
          <cfinclude template="photo-count.cfm">
        <!-- InstanceEndEditable --> 
							</td>
						</tr>
						<!---<tr>
							<td style="height:25px;">&nbsp;</td>
						</tr>--->
					</table>
		</td>
		<td width="25" id="right_shadow">&nbsp;</td>
	</tr>
	<tr>
		<td width="25" id="left_shadow">&nbsp;</td>
		<td height="35" align="right" class="bottom-text1" style="margin-right: 0px;">&nbsp;</td>
		<td id="right_shadow">&nbsp;</td>
	</tr>
	<!---<tr>
		<td width="25" id="left_shadow">&nbsp;</td>
		<td height="35" align="right" class="bottom-text1" style="margin-right: 0px;">The online Factbook is updated is updated bi-weekly. ISSN 1553-8133<br />
			For additional information on government leaders in selected foreign countries, go to World Leaders. </td>
		<td id="right_shadow">&nbsp;</td>
</tr>--->
  <tr>
	  <td width="25" id="left_shadow">&nbsp;</td>
	  <td height="35" align="center" class="classification" style="border-top: 1px solid #ccc;">UNCLASSIFIED</td>
	  <td width="25" id="right_shadow">&nbsp;</td>
  </tr>
</table>
<a href="#" class="go-top">GO TOP</a>
  <script>
	$(document).ready(function() {
		// Show or hide the sticky footer button
		$(window).scroll(function() {
			if ($(this).scrollTop() > 350) {
				$('.go-top').fadeIn(100);
			} else {
				$('.go-top').fadeOut(100);
			}
		});
		
		// Animate the scroll to top
		$('.go-top').click(function(event) {
			event.preventDefault();
			
			$('html, body').animate({scrollTop: 10}, 300);
		})
	});
</script>	

</body>
<!-- InstanceEnd --></html>
