/* grh_spotcheck.gp -- how conditional are the tabulated class groups?
 *
 *   gp -q data/grh_spotcheck.gp
 *
 * quadclassunit uses Bach's bound for the factor base and is therefore correct
 * only under GRH.  bnfinit(...) followed by bnfcertify(...) removes the
 * assumption: bnfcertify verifies the class group and regulator unconditionally
 * (it checks that the computed data is correct without assuming GRH).
 *
 * This script re-computes a sample of discriminants both ways and reports any
 * disagreement.  It is a spot check, not a proof that the whole tabulation is
 * unconditional: certifying all 3 million discriminants is far more expensive
 * than computing them.  The honest description of the datasets is therefore
 * "GRH-conditional, spot-checked unconditionally on the sample below".
 */

default(parisize, 500000000);
default(realprecision, 38);

check(D) = {
  my(v = quadclassunit(D), b, cyc1, cyc2);
  cyc1 = Vec(v[2]);
  b = bnfinit(x^2 - D, 1);
  if(!bnfcertify(b), return([-1, cyc1, []]));   /* certification failed */
  cyc2 = Vec(b.cyc);
  if(cyc1 == cyc2, [0, cyc1, cyc2], [1, cyc1, cyc2]);
};

{
  my(bad = 0, uncert = 0, tested = 0, t0 = getwalltime());
  print("range            tested  mismatches  uncertified");
  for(k = 1, 6,
    my(lo = 10^k, n = 0, b = 0, u = 0, D = lo);
    while(n < 40,
      D++;
      if(isfundamental(D) && !issquare(D),
        my(r = check(D));
        if(r[1] == 1, b++; print("  MISMATCH at D=", D, ": ", r[2], " vs ", r[3]));
        if(r[1] == -1, u++; print("  UNCERTIFIED at D=", D));
        n++));
    tested += n; bad += b; uncert += u;
    printf("10^%d..          %6d  %10d  %11d\n", k, n, b, u)
  );
  /* also sample the regulator-ordered population: D = t^2 - 4 near t = 10^5,
     which is where the class numbers are largest and the algorithm works hardest */
  my(n = 0, b = 0, u = 0, t = 10^5);
  while(n < 25,
    t++;
    my(D = t^2 - 4);
    if(isfundamental(D) && !issquare(D),
      my(r = check(D));
      if(r[1] == 1, b++; print("  MISMATCH at D=", D, ": ", r[2], " vs ", r[3]));
      if(r[1] == -1, u++; print("  UNCERTIFIED at D=", D));
      n++));
  tested += n; bad += b; uncert += u;
  printf("D=t^2-4, t~10^5 %6d  %10d  %11d\n", n, b, u);

  print();
  print("total tested      = ", tested);
  print("total mismatches  = ", bad);
  print("total uncertified = ", uncert);
  print("elapsed (ms)      = ", getwalltime() - t0);
}
quit
