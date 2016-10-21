<!doctype html>
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> 
 <!--<![endif]-->
<html class="no-js" lang="en"><!-- InstanceBegin template="/Templates/wfbext_template.dwt.cfm" codeOutsideHTMLIsLocked="false" -->
<head>
<cfset whatever = "../">
<cfinclude template="../connections/GlobalVariables.cfm">
<cfinclude template="../connections/PubYearSetter.cfm">
<cfinclude template="../connections/udfs.cfm">
<cfinclude template="../includes/print.cfm">

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <!-- InstanceBeginEditable name="doctitle" -->
  <title>The World Factbook</title>
  <!-- InstanceEndEditable -->
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width">
  <!---<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no">
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />--->
  <!--- cia.gov styles --->
  
  <link href="../css/fullscreen-external.css" rel="stylesheet" type="text/css">
  <script src="../js/modernizr-latest.js"></script><!--developers version - switch to specific production http://modernizr.com/download/--> 
  <script type="text/javascript" src="../js/jquery-1.8.3.min.js"></script>
  <script type="text/javascript" src="../js/jquery.main.js"></script>
  
  <!--- wfb styles --->
  <link rel="stylesheet" type="text/css" href="../styles/jquery.ui.core.css">
  <link rel="stylesheet" type="text/css" href="../styles/jquery.qtip.css">
  <link rel="stylesheet" type="text/css" href="../styles/listnav.css"/> 
  <link rel="stylesheet" type="text/css" href="../styles/navigation.css">
  <link rel="stylesheet" type="text/css" href="../styles/wfb_styles.css">
  <link rel="stylesheet" type="text/css" href="../scripts/galleria/themes/classic/galleria.classic.css">
  
  
  <script type="text/javascript" src="../scripts/jquery.idTabs.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="../scripts/jquery.listmenu.js"></script>
  <script type="text/javascript" src="../scripts/jquery.listnav.pack.2.1.js" charset="utf-8"></script>

  <script src="../scripts/jquery-ui-1.9.2.custom.js" type="text/javascript"></script>
  <script type="text/javascript" src="../scripts/jquery.qtip-2.0.js"></script>
  <script type="text/javascript" src="../scripts/jquery.qtip.min.js"></script>
  <script src="../scripts/imgscale.js"></script>
  <script type="text/javascript" src="../scripts/wfb_scripts.js" charset="utf-8"></script> 
  
  <!--[if IE]><script type="text/javascript" src="../js/ie.js"></script><![endif]-->
<!-- InstanceBeginEditable name="head" -->
<!-- load Galleria -->
<link rel="stylesheet" type="text/css" href="../scripts/galleria/themes/classic/galleria.classic.css">
<script src="../scripts/galleria/galleria-1.2.9.min.js"></script>
<!-- InstanceEndEditable -->
</head>
<body> 
  <noscript>Javascript must be enabled for the correct page display</noscript>
  <div id="wrapper">
    <header id="header">
      <div class="header-holder">
       	<a class="skip" accesskey="S" href="#main-content">skip to content</a>
        <span class="bg-globe"></span>
        <div class="header-panel">
          <hgroup>
              <h1 class="logo"><a href="/"><img src="../images/logo.png" alt="Central Intelligence Agency"><span>Central Intelligence Agency</span></a></h1>
              <h2 class="work-text">The Work Of A Nation. The Center of Intelligence.</h2>
          </hgroup>
          <div class="search-form">
            <div class="row">
              <div class="add-nav">
                <ul>
                  <li><a class="active" href="/contact-cia/report-threats.html">Report Threats</a></li>
                  <li><a href="/about-cia/iraqi-rewards-program.html">رعربيعربي</a></li>
                  <li><a href="/contact-cia/index.html" title="A single point of contact for all CIA inquiries.">Contact</a></li>
                </ul>
              </div>
            </div>
            <div class="row">
              <form id="ciaSearchForm" method="get" action="/search">
                <fieldset>
                  <legend class="visuallyhidden">Search CIA.gov</legend>
                  <label class="visuallyhidden" for="q">Search</label>
                  <input name="q" type="text" class="text" id="q" maxlength="2047" placeholder="Search CIA.gov..."/>
				  <input type="hidden" name="site" value="CIA" />
				  <input type="hidden" name="output" value="xml_no_dtd" />
				  <input type="hidden" name="client" value="CIA" />
				  <input type="hidden" name="myAction" value="/search" />
				  <input type="hidden" name="proxystylesheet" value="CIA" />
				  <input type="hidden" name="submitMethod" value="get" />
                  <input type="submit" value="Search" class="submit" />
                </fieldset>
              </form>
            </div>
            <div class="row">              
              <ul class="lang-list">
                <li lang="ar" xml:lang="ar"><a href="/ar/index.html">عربي</a></li>
                <li lang="zh-cn" xml:lang="zh-cn"><a href="/zh/index.html">中文</a></li>
                <li lang="en" xml:lang="en"><a href="/index.html">English</a></li>
                <li lang="fr" xml:lang="fr"><a href="/fr/index.html">Français</a></li>
                <li lang="ru" xml:lang="ru"><a href="/ru/index.html">Русский</a></li>
                <li lang="es" xml:lang="es"><a href="/es/index.html">Español</a></li>
                <li lang="en" xml:lang="en"><a title="additional-info" class="more" href="/foreign-languages/index.html">More<span class="visuallyhidden"> Languages</span></a></li>
              </ul>
            </div>
          </div>   
        </div>
        <nav id="nav">
          <h3 class="visuallyhidden">Navigation</h3>
          <ul>
            <li>
              <a href="/">Home</a>
              <span class="arrow"></span>
            </li>
            <li>
              <a href="/about-cia/">About CIA</a>
              <span class="arrow"></span>
              <div class="drop">
                <ul>
                    <li><a href="/about-cia/todays-cia/index.html">Today's CIA</a></li>
                    <li><a href="/about-cia/leadership/index.html">Leadership</a></li>
                    <li><a href="/about-cia/cia-vision-mission-values/index.html">CIA Vision, Mission &amp; Values</a></li>
                    <li><a href="/about-cia/headquarters-tour/index.html">Tour Headquarters</a></li>
                    <li><a href="/about-cia/cia-museum/index.html">CIA Museum</a></li>
                    <li><a href="/about-cia/history-of-the-cia/index.html">History of the CIA</a></li>
                    <li><a href="/about-cia/faqs/index.html">FAQs</a></li>
                    <li><a href="/about-cia/no-fear-act/index.html">NoFEAR Act</a></li>
                    <li><a href="/about-cia/site-policies/index.html">Site Policies</a></li>
                </ul>
                <div class="info-box">
                  <img src="../images/navthumb-about.jpg" alt="About CIA" />
                  <h4>About CIA</h4>
                  <p>Discover the CIA <a href="/about-cia/">history, mission, vision and values</a>. </p>
                </div>
              </div>
            </li>
            <li>
              <a href="/careers/">Careers &amp; Internships</a>
              <span class="arrow"></span>
              <div class="drop">
                <ul>
                    <li class="plain "> <a class="" href="/careers/opportunities" title="This is an overview of all career opportunities at the CIA. "> <span>Career Opportunities </span> </a> </li>
										<li class="plain "> <a class="" href="/careers/student-opportunities" title="This is the student profile page for candidates looking for jobs/ job listings at the CIA. Student Opportunities - Student Profiles"> <span>Student Opportunities</span> </a> </li>
										<li class="plain "> <a class="" href="/careers/application-process" title="How to apply to the CIA."> <span>Application Process</span> </a> </li>
										<li class="plain "> <a class="" href="/careers/life-at-cia" title="This is the about CIA section of the Careers Site"> <span>Life at CIA</span> </a> </li>
										<li class="plain "> <a class="" href="/careers/diversity" title="This is the diversity information for the Careers Site"> <span>Diversity</span> </a> </li>
										<li class="plain "> <a class="" href="/careers/military-transition" title="Your prior military service could qualify you to continue to serve your nation at the Central Intelligence Agency. Opportunities for qualified applicants are available in the U.S. and abroad."> <span>Military Transition</span> </a> </li>
										<li class="plain "> <a class="" href="/careers/games-information" title=""> <span>Diversions &amp; Information</span> </a> </li>
										<li class="plain "> <a class="" href="/careers/faq" title="Frequently Asked Questions/ FAQ for a Career at the CIA in the Careers Section"> <span>FAQs</span> </a> </li>
                </ul>
                <div class="info-box">
                  <img src="../images/navthumb-careers.jpg" alt="Careers &amp; Internships" />
                  <h4>Careers &amp; Internships</h4>
                  <p>Your talent. Your diverse skills. Our mission. Learn more about <a href="/careers/">Careers Opportunities at CIA</a>.</p>
                </div>
              </div>
            </li>
            <li>
              <a href="/offices-of-cia/">Offices of CIA</a>
              <span class="arrow"></span>
              <div class="drop">
                <ul>
                    <li class="plain "> <a class="" href="/offices-of-cia/intelligence-analysis" title=""> <span>Intelligence &amp; Analysis</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/clandestine-service" title=""> <span>Clandestine Service</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/science-technology" title=""> <span>Science &amp; Technology</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/mission-support" title=""> <span>Support to Mission</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/human-resources" title=""> <span>Human Resources</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/public-affairs" title="Public Affairs"> <span>Public Affairs</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/general-counsel" title=""> <span>General Counsel</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/equal-employment-opportunity" title=""> <span>Equal Employment Opportunity</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/congressional-affairs" title="Office of Congressional Affairs"> <span>Congressional Affairs</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/inspector-general" title="Inspector General"> <span>Inspector General</span> </a> </li>
										<li class="plain "> <a class="" href="/offices-of-cia/military-affairs" title="Military Affairs"> <span>Military Affairs</span> </a> </li>
                </ul>
                <div class="info-box">
                  <img src="../images/navthumb-offices.jpg" alt="Offices of CIA" />
                  <h4>Offices of CIA</h4>
                  <p><a href="/offices-of-cia/">Learn how the CIA is organized</a> into directorates and key offices, responsible for securing our nation.</p>
                </div>
              </div>
            </li>
            <li>
              <a href="/news-information/">News &amp; Information</a>
              <span class="arrow"></span>
              <div class="drop">
                <ul>
                    <li class="plain "> <a class="" href="/news-information/press-releases-statements" title=""> <span>Press Releases &amp; Statements</span> </a> </li>
										<li class="plain "> <a class="" href="/news-information/speeches-testimony" title=""> <span>Speeches &amp; Testimony</span> </a> </li>
										<li class="plain "> <a class="" href="/news-information/cia-the-war-on-terrorism" title=""> <span>CIA &amp; the War on Terrorism</span> </a> </li>
										<li class="plain "> <a class="" href="/news-information/featured-story-archive" title="index for featured story"> <span>Featured Story Archive</span> </a> </li>
										<li class="plain "> <a class="" href="/news-information/Whats-New-on-CIAgov" title=""> <span>What&#8217;s New Archive</span> </a> </li>
										<li class="plain "> <a class="" href="/news-information/your-news" title=""> <span>Your News</span> </a> </li>
                </ul>
                <div class="info-box">
                  <img src="../images/navthumb-news.jpg" alt="News &amp; Information" />
                  <h4>News & Information</h4>
                  <p>The most up-to-date CIA <a href="/news-information/">news, press releases, information and more</a>.</p>
                </div>
              </div>
            </li>
            <li class="active">
              <a href="/library/">Library</a>
              <span class="arrow"></span>
              <div class="drop right">
                <ul>
                    <li class="plain "> <a class="" href="/library/publications" title=""> <span>Publications</span> </a> </li>
										<li class="plain "> <a class="" href="/library/center-for-the-study-of-intelligence" title="CSI section"> <span>Center for the Study of Intelligence</span> </a> </li>
										<li class="plain "> <a class="" href="/library/foia" title=""> <span>Freedom of Information Act Electronic Reading Room</span> </a> </li>
										<li class="plain "> <a class="" href="/library/kent-center-occasional-papers" title=""> <span>Kent Center Occasional Papers</span> </a> </li>
										<li class="plain "> <a class="" href="/library/intelligence-literature" title=""> <span>Intelligence Literature</span> </a> </li>
										<li class="plain "> <a class="" href="/library/reports" title="Reports"> <span>Reports</span> </a> </li>
										<li class="plain "> <a class="" href="/library/related-links.html" title="Related Links"> <span>Related Links</span> </a> </li>
										<li class="plain "> <a class="" href="/library/video-center" title="Repository of CIA videos"> <span>Video Center</span> </a> </li>
                </ul>
                <div class="info-box">
                  <img src="../images/navthumb-library.jpg" alt="Library" />
                  <h4>Library</h4>
                  <p>Our <a href="/library/">open-source library</a> houses the thousands of documents, periodicals, maps and reports released to the public.</p>
                </div>
              </div>
            </li>
            <li class="last">
              <a href="/kids-page/">Kids' Zone</a>
              <span class="arrow"></span>
              <div class="drop right">
                <ul>
                   <li class="plain "> <a class="" href="/kids-page/k-5th-grade" title="K-5th Grade"> <span>K-5th Grade</span> </a> </li>
										<li class="plain "> <a class="" href="/kids-page/6-12th-grade" title=""> <span>6-12th Grade</span> </a> </li>
										<li class="plain "> <a class="" href="/kids-page/parents-teachers" title=""> <span>Parents &amp; Teachers</span> </a> </li>
										<li class="plain "> <a class="" href="/kids-page/games" title=""> <span>Games</span> </a> </li>
										<li class="plain "> <a class="" href="/kids-page/related-links" title=""> <span>Related Links</span> </a> </li>
										<li class="plain "> <a class="" href="/kids-page/privacy-statement" title=""> <span>Privacy Statement</span> </a> </li>
                </ul>                
                <div class="info-box">
                  <img src="../images/navthumb-kids.jpg" alt="Kids' Zone" />
                  <h4>Kids' Zone</h4>
                  <p><a href="/kids-page/">Learn more about the Agency</a> – and find some top secret things you won't see anywhere else.</p>
                </div>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </header>
    <div class="main-block">
     	<section id="main">
           <div class="heading-panel">
             <h1>Library</h1>
           </div>           
           <div class="main-holder">
             <div id="sidebar">
               <nav class="sidebar-nav">
                 <h2 class="visuallyhidden">Secondary Navigation</h2>
                 <ul>
                   <li><a class="active" href="/library/">Library</a></li>
                   <li>
                     <a href="/library/publications/">Publications</a>
                     <ul>
                       <li class="mark"><a class="active" href="/library/publications/the-world-factbook/">The World Factbook</a></li>
                       <li><a href="/library/publications/world-leaders-1/">World Leaders</a></li>
                       <li><a href="/library/publications/cia-maps-publications/">CIA Maps</a></li>
                       <li><a href="/library/publications/historical-collection-publications/">Historical Collection Publications</a></li>
                       <li><a href="/library/publications/additional-publications/">Additional Publications</a></li>
                     </ul>
                   </li>
                    <li><a href="/library/center-for-the-study-of-intelligence/">Center for the Study of Intelligence</a></li>
                    <li><a href="http://www.foia.cia.gov/">Freedom of Information Act Electronic Reading Room</a></li>
                    <li><a href="/library/kent-center-occasional-papers/">Kent Center Occasional Papers</a></li>
                    <li><a href="/library/intelligence-literature/">Intelligence Literature: Suggested Reading List</a></li>
                    <li><a href="/library/reports/">Reports</a></li>
                    <li><a href="/library/video-center/">Video Center</a></li>
                    <li><a href="/library/related-links.html">Related Links</a></li>
                 </ul>
               </nav>
             </div>
             <div id="content">
               <ul class="breadcrumbs">
                 <li><a href="/">Home</a></li>
                 <li><a href="/library/">Library </a></li>
                 <li><a href="/library/publications/">Publications</a></li>
                 <li>The World Factbook</li>
               </ul>
               <article class="description-box">
               	 <a id="main-content" tabindex="-1">&nbsp;</a>
                 <div class="text-holder-full">
			  <a name="wfbtop"></a>
				<div class="text-box" style="width: 770px; float: left;" id="wfb_data">
				
					<table width="100%" border="0" cellpadding="0" cellspacing="0" >
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
							<td>
								<!-- InstanceBeginEditable name="mainContent" -->
								<cfinclude template="countrytemplate.cfm">
								<!-- InstanceEndEditable --> 
							</td>
						</tr>
						<tr>
							<td style="height:75px;">&nbsp;</td>
						</tr>
					</table>
				</div>
                 </div>
               </article>
             </div>
           </div>
         </section> 
        <footer id="footer"><span class="divider"></span>
       <a href="#" class="logo-2"><img src="../images/logo-2.png" alt="Central Intelligence Agency"></a>
       <div class="footer-holder">
         <div class="footer-frame">

           <nav class="footer-nav"><div class="info-block">
                   
                   <h3><a href="/about-cia">About CIA</a></h3>
                   <ul><li>
                           <a href="/about-cia/todays-cia">Today's CIA</a>
                        </li>
                        <li>
                           <a href="/about-cia/leadership">Leadership</a>

                        </li>
                        <li>
                           <a href="/about-cia/cia-vision-mission-values">CIA Vision, Mission &amp; Values</a>
                        </li>
                        <li>
                           <a href="/about-cia/headquarters-tour">Headquarters Tour</a>
                        </li>

                        <li>
                           <a href="/about-cia/cia-museum">CIA Museum</a>
                        </li>
                        <li>
                           <a href="/about-cia/history-of-the-cia">History of the CIA</a>
                        </li>
                        <li>
                           <a href="/about-cia/faqs">FAQs</a>

                        </li>
                        <li>
                           <a href="/about-cia/no-fear-act">NoFEAR Act</a>
                        </li>
                        <li>
                           <a href="/about-cia/site-policies">Site Policies</a>
                        </li>
                    </ul></div>

              <div class="info-block">
                   
                   <h3><a href="/careers">Careers &amp; Internships</a></h3>
                   <ul><li>
                           <a href="/careers/opportunities">Career Opportunities </a>
                        </li>
                        <li>

                           <a href="/careers/student-opportunities">Student Opportunities</a>
                        </li>
                        <li>
                           <a href="/careers/application-process">Application Process</a>
                        </li>
                        <li>
                           <a href="/careers/life-at-cia">Life at CIA</a>

                        </li>
                        <li>
                           <a href="/careers/diversity">Diversity</a>
                        </li>
                        <li>
                           <a href="/careers/military-transition">Military Transition</a>
                        </li>
                        <li>

                           <a href="/careers/games-information">Diversions &amp; Information</a>
                        </li>
                        <li>
                           <a href="/careers/faq">FAQs</a>
                        </li>
                    </ul><h3><a href="/offices-of-cia">Offices of CIA</a></h3>

                   <ul><li>
                           <a href="/offices-of-cia/intelligence-analysis">Intelligence &amp; Analysis</a>
                        </li>
                        <li>
                           <a href="/offices-of-cia/clandestine-service">Clandestine Service</a>
                        </li>
                        <li>

                           <a href="/offices-of-cia/science-technology">Science &amp; Technology</a>
                        </li>
                        <li>
                           <a href="/offices-of-cia/mission-support">Support to Mission</a>
                        </li>
                        <li>
                           <a href="/offices-of-cia/human-resources">Human Resources</a>

                        </li>
                        <li>
                           <a href="/offices-of-cia/public-affairs">Public Affairs</a>
                        </li>
                        <li>
                           <a href="/offices-of-cia/general-counsel">General Counsel</a>
                        </li>
                        <li>

                           <a href="/offices-of-cia/equal-employment-opportunity">Equal Employment Opportunity</a>
                        </li>
                        <li>
                           <a href="/offices-of-cia/congressional-affairs">Congressional Affairs</a>
                        </li>
                        <li>
                           <a href="/offices-of-cia/inspector-general">Inspector General</a>

                        </li>
                        <li>
                           <a href="/offices-of-cia/military-affairs">Military Affairs</a>
                        </li>
                    </ul></div>


             <div class="info-block">
                   
                   <h3><a href="/news-information">News &amp; Information</a></h3>

                   <ul><li>
                           <a href="/news-information/press-releases-statements">Press Releases &amp; Statements</a>
                        </li>
                        <li>
                           <a href="/news-information/speeches-testimony">Speeches &amp; Testimony</a>
                        </li>

                        <li>
                           <a href="/news-information/cia-the-war-on-terrorism">CIA &amp; the War on Terrorism</a>
                        </li>
                        <li>
                           <a href="/news-information/featured-story-archive">Featured Story Archive</a>
                        </li>
                        <li>

                           <a href="/news-information/Whats-New-on-CIAgov">What&#8217;s New Archive</a>
                        </li>
                        <li>
                           <a href="/news-information/your-news">Your News</a>
                        </li>
                    </ul><h3><a href="/library">Library</a></h3>
                   <ul><li>

                           <a href="/library/publications">Publications</a>
                        </li>
                        <li>
                           <a href="/library/center-for-the-study-of-intelligence">Center for the Study of Intelligence</a>
                        </li>
                        <li>
                           <a href="/library/foia">Freedom of Information Act Electronic Reading Room</a>

                        </li>
                        <li>
                           <a href="/library/kent-center-occasional-papers">Kent Center Occasional Papers</a>
                        </li>
                        <li>
                           <a href="/library/intelligence-literature">Intelligence Literature</a>
                        </li>
                        <li>

                           <a href="/library/reports">Reports</a>
                        </li>
                        <li>
                           <a href="/library/related-links.html">Related Links</a>
                        </li>
                        <li>
                           <a href="/library/video-center">Video Center</a>

                        </li>
                    </ul></div>


               <div class="info-block add">
                   
                   <h3><a href="/kids-page">Kids' Zone</a></h3>
                   <ul><li>
                           <a href="/kids-page/k-5th-grade">K-5th Grade</a>
                        </li>

                        <li>
                           <a href="/kids-page/6-12th-grade">6-12th Grade</a>
                        </li>
                        <li>
                           <a href="/kids-page/parents-teachers">Parents &amp; Teachers</a>
                        </li>
                        <li>

                           <a href="/kids-page/games">Games</a>
                        </li>
                        <li>
                           <a href="/kids-page/related-links">Related Links</a>
                        </li>
                        <li>
                           <a href="/kids-page/privacy-statement">Privacy Statement</a>

                        </li>
                    </ul><h3><a href="/contact-cia">Connect with CIA</a></h3>
                   <ul class="socials-list"><li><a href="http://www.youtube.com/user/ciagov">CIA YouTube</a></li>
                     <li><a class="social-2" href="http://www.flickr.com/photos/ciagov">CIA Flickr PhotoStream</a></li>
                     <li><a class="social-3" href="/news-information/your-news">RSS</a></li>
                     <li><a class="social-4" href="/contact-cia">Contact Us</a></li>

                   </ul></div>


               </nav><div id="plugins" class="info-panel">
                    <h4>* Required plugins</h4>
                    <ul><li data-plugin="swf"><a href="http://get.adobe.com/flashplayer/">Adobe&#174; Flash Player</a></li>
                        <li data-plugin="pdf"><a href="http://get.adobe.com/reader/">Adobe&#174; Reader&#174;</a></li>

                        <li data-plugin="doc"><a href="http://www.microsoft.com/en-us/download/details.aspx?id=4">MS Word Viewer</a></li>
                    </ul></div>
         </div>
       </div>
     </footer>
    </div>
<div class="footer-panel" style="width: 990px;" align="center">
      <nav class="sub-nav" style="width: 100%; text-align: center;" >
        <h3 class="visuallyhidden">Footer Navigation</h3>
        <ul>
			<li><a href="/about-cia/site-policies/#privacy-notice" title="Site Policies">Privacy</a></li>
			<li><a href="/about-cia/site-policies/#copy" title="Site Policies">Copyright</a></li>
			<li><a href="/about-cia/site-policies/" title="Site Policies">Site Policies</a></li>
			<li><a href="http://www.usa.gov/">USA.gov</a></li>
			<li><a href="http://www.foia.cia.gov/">FOIA</a></li>
			<li><a href="http://www.dni.gov/">DNI.gov</a></li>
			<li><a href="/about-cia/no-fear-act/" title="No FEAR Act">NoFEAR Act</a></li>
			<li><a href="/offices-of-cia/inspector-general/">Inspector General</a></li>
			<li><a href="/mobile/">Mobile Site</a></li>
			<li><a href="/contact-cia/">Contact CIA</a></li>
			<li><a href="/sitemap.html">Site Map</a></li>
		</ul>
       <div style="width: 100%;" align="center"><a href="/open/" ><img src="../images/ico-06.png" width="101" height="24" alt="open gov"></a></div>
      </nav>
</div>
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
			
			$('html, body').animate({scrollTop: 350}, 300);
		})
	});
</script>	

</body>
<!-- InstanceEnd --></html>