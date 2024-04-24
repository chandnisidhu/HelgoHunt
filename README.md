# HelgoHunt
The repository hosts diamond databases comprising functionally annotated nucleotide and protein sequences derived from metagenomes sequenced during the Helgoland spring phytoplankton bloom from 2010-2020. The sequencing of these metagenomes involved extracting community DNA from subsurface seawater and filtered using a 0.2-micron pore-size filter.
These datasets were gathered within the DFG project POMPU FOR2406 (Proteogenomics of marine polysaccharide utilization).

## Functional annotation and taxonomic assignment of the sequences
Taxonomic assignment and functional annotations were performed using the SequeezeMeta pipeline v1.3.1 (Tamames & Puente-Sanchez 2019, Frontiers in Microbiology 9, 3349). ORFs were predicted with Prodigal (Hyatt et al 2010, BMC Bioinformatics 11: 119), and functional annotations were conducted through similarity searches against GenBank (Clark et al 2016, Nucleic Acids Res), eggNOG (Huerta-Cepas et al 2016, Nucleic Acids Res), and KEGG (Kanehisa and Goto 2000, Nucleic Acids Res). HMM homology searches were performed with HMMER3 (Eddy 2009, Genome Inform) against the Pfam database (Finn et al 2016, Nucleic Acids Res). The Last Common Ancestor (LCA) algorithm was employed to assign taxa to genes. Subsequently, nucleotide (.fna) and protein (.faa) files were converted into diamond databases using diamond v0.9.24.125 (Buchfink et al 2015, Nat Methods 12, 59-60).

## Graphical User Interface (GUI)
To launch the GUI, type the following in your terminal. Make sure that you're using the correct path!

python HelgoHunt-protein.py

