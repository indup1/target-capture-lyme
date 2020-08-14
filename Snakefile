SAMPLES = ["SRR2034334.1"]


rule all:
    input:
        "plots/quals.svg"

rule sra_fastq:
    input:
        "data/placeholder"
    shell:
        "./sratoolkit/bin/fastq-dump data/samples/{input}"

rule bwa_map:
    input:
        "data/refgen.fna",
        "data/samples/SRR2034334.1.fastq"
    output:
        "mapped_reads/SRR2034334.1.bam"
    shell:
        "bwa mem {input} | samtools view -Sb - > {output}"


rule samtools_sort:
    input:
        "mapped_reads/{sample}.bam"
    output:
        "sorted_reads/{sample}.bam"
    shell:
        "samtools sort -T sorted_reads/{wildcards.sample} "
        "-O bam {input} > {output}"


rule samtools_index:
    input:
        "sorted_reads/SRR2034334.1.bam"
    output:
        "sorted_reads/SRR2034334.1.bam.bai"
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