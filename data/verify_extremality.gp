/* verify_extremality.gp -- computational verification of the extremality
 * statements E1-E4 and of the refutation K1, for EXTREMALITY_NOTE.md.
 *
 *   gp -q data/verify_extremality.gp
 *
 * Every number printed here is reproduced verbatim in EXTREMALITY_NOTE.md and
 * REPORT.md under the tag [COMPUTED].
 */

default(realprecision, 40);

print("================ E1: smallest real quadratic fundamental discriminant ================");
{
  my(v = List());
  for(D = 2, 40, if(isfundamental(D) && !issquare(D), listput(v, D)));
  print("  positive fundamental discriminants (D=1 excluded: that is Q, not a field of degree 2):");
  print("    ", Vec(v)[1..12]);
  print("  minimum = ", Vec(v)[1]);
}

print();
print("================ E2: smallest regulator ================");
{
  my(L = List());
  for(D = 5, 5000, if(isfundamental(D) && !issquare(D),
     listput(L, [quadregulator(D), D])));
  L = vecsort(Vec(L), 1);
  print("  ten smallest regulators among 0 < D <= 5000:");
  for(i = 1, 10,
    my(D = L[i][2], e = quadunit(D));
    print("    R = ", L[i][1], "   D = ", D, "   eps = ", e,
          "   N(eps) = ", norm(e)));
  print("  min regulator = ", L[1][1], " at D = ", L[1][2]);
  print("  log((1+sqrt(5))/2) = ", log((1 + sqrt(5))/2));
  print("  equal? ", abs(L[1][1] - log((1+sqrt(5))/2)) < 1e-35);
  \\ The elementary bound: eps_D = (t + u sqrt D)/2 with t,u >= 1 integers and
  \\ D >= 5, hence eps_D >= (1 + sqrt 5)/2, with equality only for D = 5.
  print("  elementary bound check: min over D of (1 + sqrt(D))/2 = ",
        (1 + sqrt(5))/2, "  = phi");
  my(bad = 0);
  for(D = 5, 20000, if(isfundamental(D) && !issquare(D),
     if(quadunit(D) < (1+sqrt(5))/2 - 1e-30, bad++)));
  print("  counterexamples to eps_D >= phi for D <= 20000: ", bad);
}

print();
print("================ E3: Hurwitz constant ================");
{
  my(phi = (1 + sqrt(5))/2);
  print("  sqrt(5) = ", sqrt(5));
  print("  phi     = ", phi, "   continued fraction of phi = ", contfrac(phi)[1..12]);
  \\ liminf q ||q phi|| = 1/sqrt 5 : check numerically along convergents
  print("  q * |q phi - p| along convergents of phi (should decrease to 1/sqrt5 = ",
        1/sqrt(5), "):");
  my(cf = contfrac(phi, 25));
  for(k = 4, 14,
    my(c = contfracpnqn(cf[1..k]), p = c[1,1], q = c[2,1]);
    print("    q = ", q, "   q*|q*phi - p| = ", q * abs(q*phi - p)));
}

print();
print("================ E4: shortest primitive closed geodesic, H/PSL_2(Z) ================");
{
  my(phi = (1 + sqrt(5))/2);
  print("  hyperbolic g in SL_2(Z) needs |tr g| > 2, and tr g is an integer,");
  print("  so the minimum is |tr g| = 3, attained by [[2,1],[1,1]]:");
  my(M = [2,1;1,1]);
  print("    M = [2,1;1,1],  det = ", matdet(M), ",  trace = ", trace(M));
  print("    eigenvalues: ", polroots(charpoly(M)));
  print("    larger eigenvalue lambda = ", (3 + sqrt(5))/2,
        "   = phi^2 ? ", abs((3+sqrt(5))/2 - phi^2) < 1e-35);
  print("  translation length  l = 2 log lambda = 2 acosh(|tr|/2):");
  print("    2*log(phi^2)   = ", 2*log(phi^2));
  print("    2*acosh(3/2)   = ", 2*acosh(3/2));
  print("    4*log(phi)     = ", 4*log(phi));
  print("    all equal? ", abs(2*log(phi^2) - 2*acosh(3/2)) < 1e-35 &&
                            abs(2*log(phi^2) - 4*log(phi)) < 1e-35);
  print("  NOTE the half-length, often quoted by mistake as the length:");
  print("    acosh(3/2) = 2 log phi = ", 2*log(phi));
  print("  discriminant of the trace-3 class: t^2 - 4 = ", 3^2 - 4);
  print("  narrow (totally positive) fundamental unit of D=5:");
  print("    eps_5 = ", quadunit(5), ",  N(eps_5) = ", norm(quadunit(5)),
        "  =>  eps_5^+ = eps_5^2 = phi^2 = ", phi^2);
  print("    so l = 2 log eps_5^+ = ", 2*log(phi^2), " = 4 log phi.");
}

print();
print("================ K1: the class number carries no information here ================");
{
  print("  Minkowski bound for a real quadratic field of discriminant D is sqrt(D)/2.");
  print("  If sqrt(D)/2 < 2 then no prime ideal of norm >= 2 need be tested and h = 1");
  print("  is forced by the bound alone.  sqrt(D)/2 < 2  <=>  D < 16.");
  my(v = List());
  for(D = 2, 40, if(isfundamental(D) && !issquare(D) && sqrt(D)/2 < 2, listput(v, D)));
  print("  positive fundamental discriminants with Minkowski bound < 2:");
  for(i = 1, #v, my(D = Vec(v)[i]);
    print("    D = ", D, "   field = Q(sqrt", core(D), ")   Mink = ", sqrt(D)/2,
          "   h = ", quadclassunit(D)[1]));
  print("  count = ", #v, "  -- so h = 1 does NOT single out Q(sqrt 5).");
  print("  first D with Minkowski bound >= 2:");
  for(D = 16, 40, if(isfundamental(D) && !issquare(D),
    print("    D = ", D, "   Mink = ", sqrt(D)/2, "   h = ", quadclassunit(D)[1]); break));
  print("  smallest D > 0 with h(D) > 1:");
  for(D = 5, 500, if(isfundamental(D) && !issquare(D) && quadclassunit(D)[1] > 1,
    print("    D = ", D, "   h = ", quadclassunit(D)[1],
          "   Mink = ", sqrt(D)/2); break));
}
quit
