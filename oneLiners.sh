

# subsample 1% of bam file

samtools view -b -s 0.01 infile.bam > ten_percent_of_bam_file.bam



# bam ==> fastq
samtools bam2fq input.bam > output.fastq

# fastq ==> fasta
cat test.fastq | paste - - - - | sed 's/^@/>/g'| cut -f1-2 | tr '\t' '\n' > test.fasta

# get files from cgb
wget --user=JayLennon --password=pZ3S2a33 https://lims.cgb.indiana.edu/outbox/LennonLab/<rest-of-link>
