import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
   parser = argparse.ArgumentParser(
       description='Separates a CSV file into training and validation sets',
       formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument('input_csv',
                       metavar='input_csv',
                       type=str,
                       help='Path to the input CSV file')
   parser.add_argument(
       '-f',
       metavar='train_frac',
       type=float,
       default=.75,
       help='fraction of the dataset that will be separated for training (default .75)')
   parser.add_argument(
       '-o',
       metavar='output_dir',
       type=str,
       default=None,
       help='Directory to output train and evaluation datasets (default input_csv directory)')

   args = parser.parse_args()

   if args.f < 0 or args.f > 1:
      raise ValueError('train_frac must be between 0 and 1')

   # output_dir = input_csv directory is None
   if args.o is None:
      output_dir, _ = os.path.split(args.input_csv)
   else:
      output_dir = args.o

   df = pd.read_csv(args.input_csv)
   df = df.sort_values(by=['filename'], ascending=True)


   train_df, validation_df = train_test_split(df, test_size=None, train_size=args.f, shuffle=False)
   
   exception = train_df.merge(validation_df, on='filename', how='inner', suffixes=('_toremove', ''))
   exception.drop(exception.filter(regex='_toremove$').columns.tolist(),axis=1, inplace=True)
  
   validation_df = validation_df.merge(exception, on='filename', how='left', indicator=True, suffixes=('', '_toremove')).query('_merge == "left_only"').drop('_merge', 1)
   validation_df.drop(validation_df.filter(regex='_toremove$').columns.tolist(),axis=1, inplace=True)
   train_df = pd.concat([train_df, exception])

   # output files have the same name of the input file, with some extra stuff appended
   new_csv_name = os.path.splitext(args.input_csv)[0]
   train_csv_path = os.path.join(output_dir, new_csv_name + '_train.csv')
   eval_csv_path = os.path.join(output_dir, new_csv_name + '_eval.csv')

   train_df.to_csv(train_csv_path, index=False)
   validation_df.to_csv(eval_csv_path, index=False)