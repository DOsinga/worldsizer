<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
</head>

<body>
<cfset UMList = "fq,hq,dq,jq,kq,mq,lq,um,fs">
<cfinclude template="../connections/MS.cfm">
<cfinclude template="../connections/GlobalVariables.cfm">
<cfinclude template="../functions/funcs_getCountryImageCount.cfm">
<cfset currPath = GetDirectoryFromPath(GetCurrentTemplatePath())>

<!---<link rel="stylesheet" type="text/css" href="../scripts/media2/css/demo_page.css"/>
<link rel="stylesheet" type="text/css" href="../scripts/media2/css/jquery.dataTables.css"/>
<script type="text/javascript" language="Javascript" src="/webtools/JSCentral/JQuery/jquery-1.7.1.js"></script> 

		<script type="text/javascript" language="javascript" src="../scripts/media2/js/jquery.dataTables.js"></script>
		<script type="text/javascript" charset="utf-8">
			$(document).ready(function() {
				$('#photoCount').dataTable({
					"iDisplayLength":500,
					"iDataSort": 3});
			} );
		</script>
--->
<cfquery name="GetCountryName" datasource="wfb">
	SELECT 		CODEDESC , CODEVALUE
	FROM 		FACTBOOK.LOOKUP 
	WHERE 		pubyear = 2014
	AND 			CODETYPE = 'GEO' 
	and 			active ='Y'
  	order by 		CODEDESC , CODEVALUE
</cfquery>
<cfquery name="GetPhotoCount" datasource="wfb">
	SELECT 		count(*) as totalcount
	FROM 		FACTBOOK.photo_images
</cfquery>

<cfquery name="GetPhotoList" datasource="wfb">
	SELECT 		geocode
	FROM 		FACTBOOK.photo_images
	group by 		geocode
</cfquery>

<cfset ZeroPhotoList = ValueList(GetPhotoList.geocode,',')>
<!---
<cfdump var="#ZeroPhotoList#">


--->

<table width="100%" border="0" cellpadding="0" cellspacing="0">
<tr height="25">
		<td height="23" background="../graphics/gold_gradiant.gif"><span class="region"><strong>&nbsp; Country Photo Count</strong></span></td>
	</tr>
</table>
	<br />
	<!---Total number of photos on test = <cfoutput> <strong>#GetPhotoCount.totalcount# </strong></cfoutput><br />--->
	Total number of photos = <cfoutput> <strong>#GetPhotoCount.totalcount# </strong></cfoutput>
	<br /><br />
	<div id="demo" style="width: 100%;">
<table cellpadding="2" cellspacing="2" border="0" class="display" width="100%">
	<thead>
		<tr>
			<th align="center" bgcolor="#D6D6D6">Country Code</th>
			<th width="332" height="25" align="left" bgcolor="#D6D6D6">Country Name</th>
			<th width="433" bgcolor="#D6D6D6">Count</th>
		</tr>
	</thead>
	<tbody style="font-size: 12px;font-weight: bold;">
	<cfoutput query="GetCountryName">
	<cfif ListFindNoCase(ZeroPhotoList,codevalue) GT 0>
	<cfelse>
	<tr>
		<td width="201" align="center">#codevalue#</td>
		<td align="left"><a href="../photoUploadResize/photoUploadResize/wfbook_uploadimage.cfm?countryCode=#codevalue#" alt="  Image Upload" title="  Image Upload">#codedesc#</a></td>
		<td align="center">0</td>
	</tr>
	<!---<cfoutput>#codevalue#</cfoutput>--->
	</cfif>
	</cfoutput>
	</tbody>
	
</table>
</div><br /><br />
<div id="demo" style="width: 100%;">
<table cellpadding="2" cellspacing="2" border="0" class="display" width="100%">
	<thead>
		<tr>
			<th align="center" bgcolor="#D6D6D6">Country Code</th>
			<th width="330" height="25" align="left" bgcolor="#D6D6D6">Country Name</th>
			<th width="435" bgcolor="#D6D6D6">Count</th>
		</tr>
	</thead>
	<tbody style="font-size: 12px;font-weight: bold;">
		<cfquery name="GetCountryName2" datasource="wfb">
				SELECT 		codevalue, CODEDESC
				FROM 		FACTBOOK.LOOKUP 
				ORDER BY 		codevalue, CODEDESC
				
		</cfquery>
		
		

		<cfloop query="GetCountryName">
		
			<cfquery name="GetPhotoCount2" datasource="wfb">
				SELECT 		count(*) as totalcount, GEOCODE
				FROM 		FACTBOOK.photo_images
				WHERE		GEOCODE = '#lcase(GetCountryName.codevalue)#'
				GROUP BY		GEOCODE
			</cfquery>

			

			<cfset i = #GetPhotoCount2.totalcount#>
			<cfif i GT 0 >
			<cfoutput>
				<tr>
					<td width="201" align="center" valign="baseline">#UCase(GetPhotoCount2.geocode)#</td>
					<td align="left"><a href="../photoUploadResize/wfbook_deleteimage.cfm?countryCode=#GetPhotoCount2.geocode#" alt="  Image Delete or Caption Update" title="  Image Delete or Caption Update">#GetCountryName.CODEDESC#</a></td>
					<td align="center"> #i#</td>
				</tr>
			</cfoutput>
			<cfelse>
			</cfif>
		</cfloop>
	</tbody>
	
</table>
</div><br /><br /><br />


</body>
</html>