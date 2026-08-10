/* gen_reg_ordered.gp -- real quadratic fields enumerated by REGULATOR.
 *
 * This is a COMPLETE enumeration of every fundamental discriminant D > 0 whose
 * fundamental unit satisfies  eps_D <= TMAX, i.e. R(D) <= log TMAX.  It is NOT
 * a re-sort of a discriminant-ordered list: re-sorting {D <= X} by regulator is
 * complete only out to eps ~ sqrt(X)/2, which throws away almost the entire
 * regulator-ordered population.  The fields collected here have D as large as
 * ~TMAX^2, far beyond any feasible discriminant-ordered enumeration.
 *
 * Method.  eps_D = (t + u sqrt D)/2 with t = Tr(eps_D), s = N(eps_D) = +-1 and
 *     t^2 - D u^2 = 4 s      =>      D = (t^2 - 4 s) / u^2 .
 * Since eps_D > 1 we have t = eps_D + s/eps_D > 0 and t <= eps_D + 1, so every
 * D with eps_D <= TMAX arises from some t <= TMAX + 1.  For each such t and
 * each sign s we factor M = t^2 - 4 s, run over every u with u^2 | M, and keep
 * D = M/u^2 when D is a fundamental discriminant.  A pair (t,u) may present a
 * PROPER POWER of eps_D rather than eps_D itself; that is harmless, because the
 * set is deduplicated on D and each surviving D is then re-tested against its
 * true fundamental unit.
 *
 * Emits CSV:  D , h , s , t , cyc      (columns as in gen_disc_ordered.gp,
 * except that t = Tr(eps_D) is stored exactly instead of a rounded R, which is
 * possible here precisely because t <= TMAX.  Then
 *     eps_D = (t + sqrt(t^2 - 4 s))/2 ,   R(D) = log eps_D
 * exactly, to any desired precision.)
 *
 * Same wide-class-group convention and same GRH caveat as gen_disc_ordered.gp.
 *
 * Usage:
 *   gp -q gen_reg_ordered.gp > reg_ordered.csv
 */

TMAX = 2*10^6;

default(parisize,    600000000);
default(parisizemax, 8000000000);
default(nbthreads,   4);
default(realprecision, 38);

joinbar(v) = {
  if(#v == 0, return(""));
  my(r = Str(v[1]));
  for(i = 2, #v, r = Str(r, "|", v[i]));
  r;
};

/* all fundamental discriminants D >= 5 arising from t via D = (t^2-4s)/u^2 */
candidates(t) = {
  my(L = List(), M, f, sq, dv, D);
  for(si = 0, 1,
    M = t^2 - 4*(1 - 2*si);          /* si=0 -> s=+1 -> M=t^2-4 ; si=1 -> s=-1 */
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

export(joinbar, candidates, row, TMAX);

{
  /* ---- phase 1: candidate discriminants (cheap, parallel over t-blocks) ---- */
  my(S = List(), BLK = 50000, lo = 1);
  while(lo <= TMAX + 1,
    my(hi = min(lo + BLK - 1, TMAX + 1));
    my(out = parvector(hi - lo + 1, i, candidates(lo + i - 1)));
    for(i = 1, #out, for(j = 1, #out[i], listput(S, out[i][j])));
    lo = hi + 1
  );
  S = Set(S);

  /* ---- phase 2: keep only D whose TRUE fundamental unit has trace <= TMAX,
          then compute the class group (expensive, parallel) ---- */
  print("D,h,s,t,cyc");
  my(BLK2 = 20000, n = #S, lo2 = 1);
  while(lo2 <= n,
    my(hi2 = min(lo2 + BLK2 - 1, n));
    my(Ds = vector(hi2 - lo2 + 1, i, eval(S[lo2 + i - 1])));
    my(keep = parvector(#Ds, i, if(abs(trace(quadunit(Ds[i]))) <= TMAX, Ds[i], 0)));
    my(K = select(x -> x != 0, keep));
    if(#K > 0,
      my(out = parvector(#K, i, row(K[i])));
      for(i = 1, #out, print(out[i]))
    );
    lo2 = hi2 + 1
  );
}
quit
