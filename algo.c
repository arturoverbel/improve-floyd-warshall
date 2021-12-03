/* Ismail Hakki Toroslu
September 1, 2021
Improved Floyd-Warshall Algorithm
Two lists, inlist and outlist, can be implemented
more efficiently as linked lists.
For simplicity simple array implementation is used.
*/
#include <stdio.h>
#include <stdlib.h>
#define MAXN 1025 // Maximum number of nodes
#define INF 9999 // Used as inifnity

int A[MAXN][MAXN]; // Adjaceny matrix
void new_fw(int N) {
    int inc[MAXN],outc[MAXN]; // counts of in/out edges
    
    // List of vertices incoming/outgoing to/from
    int inlist[MAXN][MAXN], outlist[MAXN][MAXN];
    int i,j,k,kk;
    int select_k[MAXN], mininxout, mink; // choose the "best" k
    
    for (i=0;i<N;i++)
        inc[i]=0,outc[i]=0,select_k[i]=0;
    
    // Generate initial inlist and outlist for each vertex
    for (i=0;i<N;i++)
        for (j=0;j<N;j++) {
            if ((A[i][j]!=0) && (A[i][j]<INF))
                inc[j]++, outc[i]++,
            inlist[j][inc[j]-1]=i, outlist[i][outc[i]-1]=j;
        }

    // The outer loop
    for (kk=0;kk<N;kk++) {
        // choose the "best" k
        mink=-1;
        mininxout=2*N*N;
        for (k=0;k<N;k++) {
            if ((select_k[k]==0) &&(inc[k]*outc[k]<mininxout)) {
                mink=k;
                mininxout=inc[k]*outc[k];
            }
        }
    
        k=mink; // "best" k
        select_k[k]=1; // remove selected vertex
        // explore only useful relaxation attempts
        for (i=0;i<inc[k];i++)
            for (j=0;j<outc[k];j++) {
                if ((A[inlist[k][i]][k]+A[k][outlist[k][j]])<A[inlist[k][i]][outlist[k][j]]){
                    if (A[inlist[k][i]][outlist[k][j]]==INF) {
                        outc[inlist[k][i]]++;
                        outlist[inlist[k][i]][outc[inlist[k][i]]-1]=
                        outlist[k][j];
                        inc[outlist[k][j]]++;
                        inlist[outlist[k][j]][inc[outlist[k][j]]-1]=
                        inlist[k][i];
                    }
                    A[inlist[k][i]][outlist[k][j]]= A[inlist[k][i]][k]+A[k][outlist[k][j]];
                }
            }
    }

    printf("Improved FW APSP\n");
    for (i=0;i<N;i++,printf("\n"))
        for (j=0;j<N;j++)
            if (A[i][j] != INF) printf("%d ",A[i][j]);
            else printf("X "); // print "X" instead of infinity
}


int main() {
    int N, i, j;
    // input N and adjacency matrix (infinity is 9999)
    scanf("%d",&N);
    for(i=0;i<N;i++)
        for(j=0;j<N;j++)
            scanf("%d",&A[i][j]);
    new_fw(N);
    
    return 0;
}