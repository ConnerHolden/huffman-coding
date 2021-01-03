# Table of Contents

[*Introduction*](#introduction)  
[*What is Huffman Coding?*](#what_is_huffman_coding?)

## Introduction

This is a Huffman Coding project for learning Python using Bhrigu Srivastava's [demo](https://github.com/bhrigu123/huffman-coding).

## What is Huffman Coding?

Compression is transforming one form of data to another that uses less space. Huffman Coding replaces data with bit sequence code values. These values are assigned in such a way that the characters appearing the most are given the shortest code values. Also, values are assigned such that the prefixes of any given code are never alike.

The first step is to build a Huffman tree. The frequency of each character must be calculated and then inserted into a priority queue. The two nodes with the smallest character frequencies are extracted from the queue, merged into a parent node (by summing their frequencies), then reinserted back into the priority queue. This process is repeated until only one root node remains in the queue.

The next step is to assign a bit value to each *path* between nodes in the tree. Each parent node has two paths (one per child node). For every parent node, one path is assigned "0" and the other "1" until the entire tree has been traversed. In the end, the path to each child from a parent should have a bit value assigned to it. The code for any given character is the concatenation of the bit values for the path taken from the root node to the character node itself.

This process yields codes where no two share the same prefixes and where the smallest of these are assigned to the most frequently occuring characters. This new compressed file will be smaller than the original. It is decompressed by reading the bits, replacing a code with its character as soon as a valid code is encountered.