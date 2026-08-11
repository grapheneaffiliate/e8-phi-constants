/* gen_reg_ordered_ext.gp -- INCREMENTAL extension of the regulator-ordered
 * enumeration from eps_D <= TMIN up to eps_D <= TMAX.
 *
 * gen_reg_ordered.gp already produced every fundamental discriminant with
 * Tr(eps_D) <= TMIN.  Rerunning it with a larger bound would recompute all of
 * those class groups again.  This script emits ONLY the new fields, so that
 *
 *     reg_ordered.csv  UNION  reg_ordered_ext.csv
 *
 * is exactly the complete enumeration up to eps_D <= TMAX.  (Verified on a small
 * range: full(2e4) == full(1e4) U ext(1e4,2e4), disjoint, 39657 rows each way.)
 *
 * Processing is BLOCK-WISE IN t rather than "collect every candidate, then
 * compute".  Two reasons:
 *
 *   (1) Memory.  The global candidate set for t up to 5*10^6 is ~10^7 integers
 *       held at once, and PARI gives each of nbthreads threads its own stack up
 *       to parisizemax; a large parisizemax then risks the OOM/segfault that a
 *       9 GB setting produced here.  Block-wise, the live set is ~10^5.
 *   (2) Partial output is complete by construction.  Rows are emitted in
 *       increasing t, and a field is emitted in the block containing its OWN
 *       t_D, so output through block ending at t gives exactly the complete
 *       enumeration out to eps_D <= t.  A run stopped early is still a usable,
 *       complete dataset at a smaller bound.
 *
 * Each kept D is emitted EXACTLY ONCE: the phase-2 test requires t_D to lie in
 * (TMIN, TMAX] *and* in the current block.  A candidate arising from a proper
 * power of eps_D has its t_D in an earlier block (or below TMIN) and is dropped
 * here, having already been emitted there (or in the old file).
 *
 * Same columns, conventions, and GRH caveat as gen_reg_ordered.gp.
 *
 * Usage:  gp -q gen_reg_ordered_ext.gp > reg_ordered_ext.csv
 */

TMIN = 2*10^6;
TMAX = 5*10^6;
BLK  = 50000;

default(parisize,     400000000);   /* per-thread; 4 threads */
default(parisizemax, 1500000000);   /* worst case ~6 GB total on a 15 GB box */
default(nbthreads,   4);
default(realprecision, 38);

joinbar(v) = {
  if(#v == 0, return(""));
  my(r = Str(v[1]));
  for(i = 2, #v, r = Str(r, "|", v[i]));
  r;
};

candidates(t) = {
  my(L = List(), M, f, sq, dv, D);
  for(si = 0, 1,
    M = t^2 - 4*(1 - 2*si);
    if(M <= 0, next);
    f  = factor(M);
    sq = prod(i = 1, #f~, f[i,1]^(f[i,2] \ 2));
    dv = divisors(sq);
    for(j = 1, #dv,
      D = M / dv[j]^2;
      if(D >= 5 && !issquare(D) && isfundamental(D), listput(L, D))
    )
  );
  Vec(L);
};

row(D) = {
  my(v = quadclassunit(D), h = v[1], cyc = Vec(v[2]),
     e = quadunit(D), t = abs(trace(e)), s = norm(e));
  Str(D, ",", h, ",", s, ",", t, ",", joinbar(cyc));
};

export(joinbar, candidates, row, TMIN, TMAX);

{
  print("D,h,s,t,cyc");
  my(lo = TMIN + 1);
  while(lo <= TMAX,
    my(hi = min(lo + BLK - 1, TMAX));
    /* candidates from this t-block */
    my(out = parvector(hi - lo + 1, i, candidates(lo + i - 1)));
    my(S = List());
    for(i = 1, #out, for(j = 1, #out[i], listput(S, out[i][j])));
    S = Set(S);
    my(Ds = vector(#S, i, eval(S[i])));
    /* keep D whose OWN fundamental-unit trace lies in this block */
    my(keep = parvector(#Ds, i,
      my(td = abs(trace(quadunit(Ds[i]))));
      if(td >= lo && td <= hi && td > TMIN && td <= TMAX, Ds[i], 0)));
    my(K = select(x -> x != 0, keep));
    if(#K > 0,
      my(res = parvector(#K, i, row(K[i])));
      for(i = 1, #res, print(res[i]))
    );
    lo = hi + 1
  );
}
quit
