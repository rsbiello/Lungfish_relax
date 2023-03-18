#! /usr/bin/env python
# Count singletons per species and print AA (private and conserved)
import sys
import pandas as pd

fasta_file = sys.argv[1]  # Input fasta file
count_file = sys.argv[2] # Output count file
singleton_sites_file = sys.argv[3] # Output singleton file
conserved_sites_file = sys.argv[4] # Output conserved file

fasta=pd.read_csv(fasta_file, sep=',', header = None)
seqs=fasta[fasta[0].str.contains('>')==False]

seqs_split=seqs[0].str.split('', expand=True)
seqs_species=seqs_split.rename(index=({1:'Ambystoma_mexicanum',3:'Anguilla_anguilla', 5:'Anolis_carolinensis', 7:'Callorhinchus_milii', 9:'Cynops_orientalis', 11:'Danio_rerio', 13:'Gallus_gallus', 15:'Homo_sapiens', 17:'Lepidosiren_paradoxa', 19:'Lepisosteus_oculatus', 21:'Monodelphis_domestica', 23:'Neoceratodus_forsteri', 25:'Protopterus_aethiopicus', 27:'Protopterus_annectens', 29:'Protopterus_dolloi'}))

nunique = seqs_species.nunique()
cols_to_drop = nunique[nunique == 1].index
seqs_variants=seqs_species.drop(cols_to_drop, axis=1)

## Create DF singleton positions
df_singletons=pd.DataFrame()
for col in seqs_variants:
    sings=seqs_variants[~seqs_variants.groupby(col)[col].transform('size').gt(13)]
    if not sings.empty:
        sings_df=sings[col].to_frame()
        df_singletons=pd.concat([df_singletons, sings_df], axis = 1, sort=True)

## Print singletons positions
null_cols=df_singletons.columns[~df_singletons.isnull().any()]
df_singletons_filt=df_singletons.drop(null_cols, axis = 1)
df_singletons_filt.to_csv(singleton_sites_file, header=True, na_rep='NaN', index=True, sep='\t', mode='w')

## Print count singletons per species
count=df_singletons_filt.count(axis=1)
count.to_csv(count_file, header=False, na_rep='NaN', index=True, sep='\t', mode='w')

## Create DF conserved positions
df_conserved=pd.DataFrame()
for col in seqs_variants:
    cons=seqs_variants[seqs_variants.groupby(col)[col].transform('size').gt(13)]
    if not cons.empty:
        cons_df=cons[col].to_frame()
        df_conserved=pd.concat([df_conserved, cons_df], axis = 1, sort=True)

## Print conserved positions
df_conserved.to_csv(conserved_sites_file, header=True, na_rep='NaN', index=True, sep='\t', mode='w')