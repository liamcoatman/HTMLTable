"""
Created on Mon Oct  6 12:43:36 2014

@author: lc585
"""

import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord

df_html = pd.read_csv('df.csv')

# """
# Change order of columns
# """

tb_html = [['NAME', 'Show', 'String'],
           ['INSTR', 'Show', 'String'],
           ['RA', 'Hide', 'String'],
           ['DEC', 'Hide', 'String'],
           ['z', 'Hide', 'Number'],
           ['DR12_NAME', 'Hide', 'String']]
          

tb_html = np.array(tb_html)

cols = list(tb_html[:, 0])  
df_html = df_html[cols]

hide_cols_ind = list(np.where(tb_html[:, 1] == 'Hide')[0])  

sort_types = list(tb_html[:, 2])

sel_cols = ['INSTR']

sel_cols_ind = [cols.index(c) for c in sel_cols]

########################################################################################################################################

def make_link(row):
        
    c = SkyCoord(row.RA, row.DEC)
    fstem = 'http://skyserver.sdss.org/dr12/en/tools/explore/summary.aspx?'
    oblink = 'ra={}&dec={}'.format(c.ra.deg, c.dec.deg)
    
    return fstem + oblink 

boss_links = df_html.apply(make_link, axis=1).values  


lines = ""
j = 0 

for idx, row in df_html.iterrows():

    for i, p in enumerate(row):

        if (i == cols.index('DR12_NAME')) & (p != 'None'):
            st = "<A HREF = " + boss_links[j] + ">" + str(p) + "</A>"

        else:
            st = str(p)

        if i == 0:
            line = "<TR><TD>" + st + "</TD>"

        elif i == len(row) - 1:
            line += "<TD>" + st + "</TD></TR>\n"

        else:
            line += "<TD>" + st + "</TD>"

    lines += line
    j += 1 

header_list = df_html.columns 

heads = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<title> Liam's Table </title>

<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
  
<style type="text/css" media="screen">

body{margin:15px; 
     padding:15px; 
     border:1px solid #666; 
     font-family:Arial, Helvetica, sans-serif; 
     font-size:88%;}

h2{margin-top: 50px;}

pre{margin:5px; 
    padding:5px;
    background-color:#f4f4f4; 
    border:1px solid #ccc; }

th img{ border:0; }

th a{color:#fff; 
     font-size:13px; 
     text-transform: uppercase; 
     text-decoration:none; }

header {
    background-color:black;
    color:white;
    text-align:center;
    padding:5px;   
}


</style>

<script src="TableFilter/tablefilter_min.js" language="javascript" type="text/javascript"></script>

<script src="TableFilter/TF_Modules/tf_paging.js" language="javascript" type="text/javascript"></script>

<link rel="stylesheet" type="text/css" href="includes/SyntaxHighlighter/Styles/SyntaxHighlighter.css" />

<script src="includes/SyntaxHighlighter/Scripts/shCore.js" language="javascript" type="text/javascript"></script>

<script src="includes/SyntaxHighlighter/Scripts/shBrushJScript.js" language="javascript" type="text/javascript"></script>

<script src="includes/SyntaxHighlighter/Scripts/shBrushXml.js" language="javascript" type="text/javascript"></script>

<script language="javascript" type="text/javascript">

//<![CDATA[tf_AddEvent(window,'load',initHighlighter);function initHighlighter()

{dp.SyntaxHighlighter.ClipboardSwf = "includes/SyntaxHighlighter/Scripts/clipboard.swf"; dp.SyntaxHighlighter.HighlightAll("code"); }

function hideIESelects(){if(tf_isIE){var slc = tf.tbl.getElementsByTagName('select');for(var i=0; i<slc.length; i++)slc[i].style.visibility = 'hidden';}}

function showIESelects(){if(tf_isIE){var slc = tf.tbl.getElementsByTagName('select');for(var i=0; i<slc.length; i++)slc[i].style.visibility = 'visible';}}//]]>

</script>

</head>

<body>

  <header>
  <h1>NIR QSO Spectra</h1>
  </header>
  <BR> 
  Options
  <BR>
  <ul>
  <li>Click the link in the 'DR12_NAME' column to go to the SDSS object page</li>
  <li>If heading is in bold hover mouse pointer over for more info </li>
  <table id="table1" cellpadding="0" cellspacing="0">
  <thead>
  <tr>

"""

for i, head in enumerate(header_list):

    if head == 'DR12_NAME':
        heads += "<TH><B><a href='#' title='Click to go to DR12 spectra page' style='color:black'>" + head + "</a></B></TH>"                                                                    

    else:   
        heads += "<TH><B>" + head + "</B></TH>"

heads += "\n</TR>\n</THEAD>\n<TBODY>\n"

tails = """
</div>
<div style="clear:both"></div> 
<script language="javascript" type="text/javascript">
//<![CDATA[
var props = {
    filters_row_index: 1,
    sort: true,
    sort_config: {sort_types:["""

tails += ', '.join("'{0}'".format(w) for w in sort_types) + ']}, \n'

for i in sel_cols_ind:
    tails += "col_{}: 'select',".format(i)

tails += """
remember_grid_values: true,
alternate_rows: true,
paging: true,
results_per_page: ['Results per page',[10,25,50,100,1000]],
rows_counter: true,
rows_counter_text: "Displayed rows: ",
btn_reset: true,
btn_reset_text: "Clear",
btn_text: ">",
loader: true,
loader_text: "Filtering data...",
loader_html: '<img src="loader.gif" alt="" style="vertical-align:middle;" /> Loading...',
on_show_loader: hideIESelects, //IE only: selects are hidden when loader visible
on_hide_loader: showIESelects, //IE only: selects are displayed when loader closed
display_all_text: "< Show all >",
extensions: {   
    name:["ColsVisibility"],  
    src:["TableFilter/TFExt_ColsVisibility/TFExt_ColsVisibility.js"],   
    description:["Columns visibility manager"],  
    initialize:[function(o){o.SetColsVisibility();}]   
}, 
showHide_cols_at_start: 
"""
tails += str(hide_cols_ind) 

tails +=  """
,  
    showHide_cols_text: "Columns: ",  
    showHide_enable_tick_all: true  
    }
var tf = setFilterGrid("table1",props);
//]]>
</script>
</body>
</html>
"""

lines = heads + lines + tails

with open('index.html', 'w') as f:
    f.write(lines)


