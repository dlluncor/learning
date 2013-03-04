
import simplejson

class Constants:
  COL_TO_DEC = {
    1: 0.00,
    2: 0.01,
    3: 0.02,
    4: 0.03,
    5: 0.04,
    6: 0.05,
    7: 0.06,
    8: 0.07,
    9: 0.08,
    10: 0.09
  }

def parseZscoreTsv(inputfile, outputfile):
  zscore_to_cdf = {}
  tsv = open(inputfile, 'r')
  col_to_dec = Constants.COL_TO_DEC
  for line in tsv.readlines():
    els = line.split('\t')
    if not els:
      continue
    if els[0] == 'z':
      continue
    first_part = float(els[0])
    for index in xrange(len(els)):
      if index == 0:
        continue
      second_part = float(col_to_dec[index])
      zscore = first_part + second_part
      if first_part < 0:
        zscore = first_part - second_part
      print zscore
      cdf = els[index].replace('\n', '')
      zscore_as_str = '%.2f' % zscore
      zscore_to_cdf[zscore_as_str] = cdf

  print_out_dict = simplejson.dumps(zscore_to_cdf)
  print print_out_dict
  fd = open(outputfile, 'w')
  fd.write('var ztable = %s;' % print_out_dict)
  fd.close()

def main():
  parseZscoreTsv('zscore.tsv', 'ztable.js')   

if __name__ == '__main__':
  main()
