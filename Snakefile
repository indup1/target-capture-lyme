SAMPLES = ["SRR2034334.1"]


rule all:
    input:
        "plots/quals.svg"

rule sra_fastq:
    input:
        "data/samples/selfgen/10081004.l10081004.000H3LCYN.1.fasta"
    shell:
        "./seqtk/seqtk seq -F '!' {input} >
data/samples/selfgen/10081004.l10081004.000H3LCYN.1.fastq"
        # "./sratoolkit/bin/fastq-dump --fasta {input}"


rule bwa_map:
    input:
        "data/refgen.fna",
        "data/samples/selfgen/10081004.l10081004.000H3LCYN.1.fastq"
    output:
        "mapped_reads/10081004.l10081004.000H3LCYN.1.bam"
    shell:
        "bwa mem {input} | samtools view -Sb - > {output}"


rule samtools_sort:
    input:
        "mapped_reads/10081004.l10081004.000H3LCYN.1.bam"
    output:
        "sorted_reads/10081004.l10081004.000H3LCYN.1.bam"
    shell:
        "samtools sort -T {input} " 
        "-O bam {input} > {output}"


rule samtools_index:
    input:
        "sorted_reads/10071001.l10071001.000H3LCYN.1.bam"
    output:
        "sorted_reads/10071001.l10071001.000H3LCYN.1.bam.bai"
    shell:
        "samtools index {input}"


rule bcftools_call:
    input:
        fa="data/refgen.fna",
        bam=expand("sorted_reads/{sample}.bam", sample=SAMPLES),
        bai=expand("sorted_reads/{sample}.bam.bai", sample=SAMPLES)
    output:
        "calls/all.vcf"
    shell:
        "samtools mpileup -g -f {input.fa} {input.bam} | "
        "bcftools call -mv - > {output}"


rule plot_quals:
    input:
        "calls/all.vcf"
    output:
        "plots/quals.svg"
    script:
        "scripts/plot-quals.py"

#./samtools/samtools depth sorted_reads/....bam -a -o depths/....txt