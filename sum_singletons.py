#! /usr/bin/env python
# Sum singletons per species and print them
import pandas as pd
import glob
import os
import sys

count_file=sys.argv[1] ## Output count files
sums_file=sys.argv[2] ## Output sum singleton file

## load path
input_path=r'.'

## get the files from the path 
input_files=glob.glob(os.path.join(input_path, '*_count_singletons'))  

## create DF with singleton count from every gene
single_count_file_list=[]
for f in input_files:
    single_count=pd.read_csv(f, header=None)
    single_count=single_count.add_suffix(f'_{f}')
    single_count_file_list.append(single_count)

single_count_genes=pd.concat(single_count_file_list, axis=1)

## Optional to remove the filename extension
single_count_genes.columns=single_count_genes.columns.str.replace('0_./', '')
single_count_genes.columns=single_count_genes.columns.str.replace('_count_singletons', '')

## Keep only count
SC_genes=single_count_genes.apply(lambda x: x.str.replace(r'^.*\t\s*', ''))

## Replace index with species names
SC_gene_def=SC_genes.rename(index=({0:'Ambystoma_mexicanum',1:'Anguilla_anguilla', 2:'Anolis_carolinensis', 3:'Cynops_orientalis', 4:'Danio_rerio', 5:'Gallus_gallus', 6:'Homo_sapiens', 7:'Lepidosiren_paradoxa', 8:'Lepisosteus_oculatus', 9:'Monodelphis_domestica', 10:'Neoceratodus_forsteri', 11:'Protopterus_aethiopicus', 12:'Protopterus_annectens', 13:'Protopterus_dolloi'}))

## Print DF with singleton count per each gene
SC_gene_def.to_csv(count_file, header=True, na_rep='NaN', index=True, sep='\t', mode='w')

## Sum all singletons
sum_SC_gene_def=SC_gene_def.astype(int)
sums_SC=sum_SC_gene_def.sum(axis=1)

## Print sum
sums_SC.to_csv(sums_file, header=True, na_rep='NaN', index=True, sep='\t', mode='w')