import StringIO
import base64
import os
import psycopg2
import psycopg2.extras
os.environ['MPLCONFIGDIR']= '/tmp'
import matplotlib
import matplotlib.cbook
matplotlib.use("Agg")
import matplotlib.pyplot as pl

def application(environ, start_response):
  status = '200 OK'
  output = '<html>'
  output += '<head>'
  output += '<title>Operating System Sucks-Rules-O-Meter</title>'
  output += '</head>'
  output += '<body>'
  output += '<h1>Operating System Sucks-Rules-O-Meter</h1>'
  try:
    # Connect to db
    conn = psycopg2.connect(database='srom', user='srom_reader', host='server.local')
    curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Get the current results from Bing
    curr.execute("SELECT * FROM results_view WHERE name = 'Bing' AND date_trunc('day', updated) = (SELECT max(date_trunc('day', updated)) FROM results_view WHERE name = 'Bing');")
    rows = curr.fetchall()
    curr.close()
    conn.close()
    X = range(len(rows))
    Y1 = []
    Y2 = []
    terms = []
    updated = ""
    for row in rows:
      terms.append(row['term'])
      Y1.append(row['positive_count'])
      Y2.append(-row['negative_count'])
      updated = row['updated']
    
    # Generate the plot  
    ax = pl.axes(frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().tick_left()

    pl.barh(X, Y1, color='green')
    pl.barh(X, Y2, color='red')
    
    padding = 0.15 * (max(Y1) - min(Y2))

    # need to calculate a padding factor
    pl.xlim(min(Y2) - padding, max(Y1) + padding)
    
    X = map((lambda x: x + 0.4), X)
    
    for x, y in zip(X, Y1):
      pl.text(y + padding/12, x, '%d' % y, ha='left', va='center')
    for x, y in zip(X, Y2):
      pl.text(y - padding/12, x, '%d' % -y, ha='right', va='center')
      
    pl.yticks(X, terms)
    pl.text(min(Y2) / 2, len(X) + 1, 'sucks', ha='center', va='center')
    pl.text(max(Y1) / 2, len(X) + 1, 'rocks/rules', ha='center', va='center')
    
    pl.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    
    # Generate an SVG string for the plot       
    imageString = StringIO.StringIO()
    pl.savefig(imageString, dpi=150, format='svg')
    output += imageString.getvalue()
    imageString.close()
#    pl.savefig(imageString, dpi=100, format='png')
#    image64 = base64.b64encode(imageString.getvalue())
#    imageString.close()
#    img_tag = '<img alt="test" src="data:image/svg;base64,{0}">'.format(image64)
#    output += img_tag

    output += '<br>'
    output += '<h3 align="right">Last updated '
    output += str(updated)
    output += '</h3>'
 
    output += '<p><a href="http://srom.zgp.org">Visit the original</a>'
    output += '<p>This operating system quality metric approval is based on a periodic '
    output += '<a href="http://www.bing.com">Bing</a> search for each of several operating'
    output += ' systems, directly followed by "sucks", "rules", or "rocks".'
    
    output += '<h4>To Do:</h4>'
    output += '<ul>'
    output += '<li>Put the scripts on Github with GPL license</li>'
    output += '<li>Make a FAQ</li>'
    output += '<li>Port to flask?</li>'
    output += '</ul>'
    
  except Exception as exc:
    errorString = traceback.format_exc()
    output += '<h2>Oops!</h2>'
    output += '<p>Looks like its broken.'
    
  output += '</body>'
  output += '</html>'

  
  # Send it
  response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]
  start_response(status, response_headers)
  return [output]
