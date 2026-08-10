/* gen_disc_window.gp -- CONTROL SAMPLE.
 *
 * The regulator-ordered dataset reaches D ~ 4*10^12, while the
 * discriminant-ordered dataset stops at D = 10^7.  Any difference between the
 * two could in principle be blamed on the size of D rather than on the
 * regulator condition.  This script removes that objection directly: it
 * enumerates consecutive fundamental discriminants in a narrow window at
 * D ~ 10^12 -- the same scale as the regulator-ordered population -- with no
 * regulator condition imposed.
 *
 * If the p-part statistics here match the discriminant-ordered ones at
 * D ~ 10^7, then D-size is not the operative variable and the difference seen
 * in the regulator ordering is due to the regulator condition.
 *
 * Emits the same CSV columns as gen_disc_ordered.gp:  D , h , s , R , cyc
 *
 * Usage:  gp -q gen_disc_window.gp > disc_window.csv
 */

DSTART = 10^12;
NWANT  = 250000;

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
  my(lo = DSTART, done = 0, CH = 100000);
  while(done < NWANT,
    my(hi = lo + CH - 1, Ds = List());
    for(D = lo, hi, if(isfundamental(D) && !issquare(D), listput(Ds, D)));
    Ds = Vec(Ds);
    if(#Ds > 0,
      my(out = parvector(#Ds, i, row(Ds[i])));
      for(i = 1, #out, if(done < NWANT, print(out[i]); done++))
    );
    lo = hi + 1
  );
}
quit
