/* gen_disc_ordered.gp -- real quadratic fields enumerated by DISCRIMINANT.
 *
 * Emits CSV:  D , h , s , R , cyc
 *   D    fundamental discriminant, 0 < D <= XMAX
 *   h    class number of the maximal order, ORDINARY (wide) sense
 *   s    N(eps_D) in {+1,-1}   (eps_D = fundamental unit > 1)
 *   R    regulator log(eps_D), 15 significant digits
 *   cyc  invariant factors of Cl(D), decreasing, '|'-separated ('' when h=1)
 *
 * The fundamental unit itself is NOT stored: its trace already has ~2700
 * decimal digits at D ~ 10^7.  R and s determine everything used downstream.
 * L(1,chi_D) is not stored either; it is recovered exactly from the analytic
 * class number formula  L(1,chi_D) = 2 h R / sqrt(D)  (see analysis/).
 *
 * CONVENTION (verified, not assumed): PARI's quadclassunit returns the
 * ORDINARY (wide) class group.  Check: quadclassunit(12)[1] = 1, whereas the
 * NARROW class number of Q(sqrt 3) is 2.  Cohen-Lenstra for real quadratic
 * fields is a statement about the ordinary class group; for ODD p the narrow
 * and wide p-parts agree anyway (they differ by a 2-group), so this study is
 * insensitive to the choice.
 *
 * GRH: quadclassunit uses Bach's bound and is therefore conditional on GRH.
 * This is standard for class-group tabulation at this scale.  An unconditional
 * cross-check on a sample is in data/grh_spotcheck.gp.
 *
 * Usage:
 *   gp -q gen_disc_ordered.gp > disc_ordered.csv
 */

XMAX  = 10^7;
CHUNK = 200000;

default(parisize,    400000000);
default(parisizemax, 6000000000);
default(nbthreads,   4);
default(realprecision, 38);

joinbar(v) = {
  if(#v == 0, return(""));
  my(r = Str(v[1]));
  for(i = 2, #v, r = Str(r, "|", v[i]));
  r;
};

row(D) = {
  my(v = quadclassunit(D), h = v[1], cyc = Vec(v[2]), R = v[4],
     s = norm(quadunit(D)));
  Str(D, ",", h, ",", s, ",", Strprintf("%.12f", R), ",", joinbar(cyc));
};

export(joinbar, row);

{
  print("D,h,s,R,cyc");
  my(lo = 5);
  while(lo <= XMAX,
    my(hi = min(lo + CHUNK - 1, XMAX), Ds = List());
    for(D = lo, hi, if(isfundamental(D) && !issquare(D), listput(Ds, D)));
    Ds = Vec(Ds);
    if(#Ds > 0,
      my(out = parvector(#Ds, i, row(Ds[i])));
      for(i = 1, #out, print(out[i]))
    );
    lo = hi + 1
  );
}
quit
