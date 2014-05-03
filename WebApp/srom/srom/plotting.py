import os
import StringIO
import psycopg2
import psycopg2.extras
os.environ['MPLCONFIGDIR']= '/tmp'
import matplotlib
import matplotlib.cbook
matplotlib.use("Agg")
import matplotlib.pyplot as pl

def getPlot():
  queryString = """
  SELECT * 
  FROM results_view 
  WHERE name = 'Bing' 
    AND date_trunc('day', updated) = 
      (SELECT max(date_trunc('day', updated)) 
       FROM results_view
       WHERE name = 'Bing')
  ORDER BY term DESC;
  """
  output = ""
  updated = ""
  
  try:
    # Connect to db
    conn = psycopg2.connect(database='srom', user='srom_reader', host='10.9.73.10')
    curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Get the current results from Bing
    curr.execute(queryString)
    rows = curr.fetchall()
    curr.close()
    conn.close()
    
    # Parse the results
    X = range(len(rows))
    Y1 = []
    Y2 = []
    terms = []
    for row in rows:
      terms.append(row['term'])
      Y1.append(row['positive_count'])
      Y2.append(-row['negative_count'])
      updated = row['updated']
    
    # Generate the plot  
    pl.figure(figsize=(10, 5))
    
    # Frame formatting
    ax = pl.axes(frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().tick_left()

    # Plot the goods
    pl.barh(X, Y1, color='green', linewidth=0)
    pl.barh(X, Y2, color='red', linewidth=0)
    
    # Calculate a padding factor for labels
    padding = 0.15 * (max(Y1) - min(Y2))

    pl.xlim(min(Y2) - padding, max(Y1) + padding)
    
    X = map((lambda x: x + 0.4), X)
    
    # Add text labels for the results
    for x, y in zip(X, Y1):
      pl.text(y + padding/12, x, '%d' % y, ha='left', va='center')
    for x, y in zip(X, Y2):
      pl.text(y - padding/12, x, '%d' % -y, ha='right', va='center')
      
    # Add in the top labels
    pl.yticks(X, terms)
    pl.text(min(Y2) / 2, len(X) + 1, 'sucks', ha='center', va='center')
    pl.text(max(Y1) / 2, len(X) + 1, 'rocks/rules', ha='center', va='center')
    
    pl.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    
    # Generate an SVG string for the plot       
    imageString = StringIO.StringIO()
    pl.savefig(imageString, dpi=150, format='svg')
    output = imageString.getvalue()
    imageString.close()
  
  except Exception as exc:
    output += '<h2>Oops!</h2>'
    output += '<p>Looks like its broken.'
    updated = 'N/A'
    
  return output, updated
