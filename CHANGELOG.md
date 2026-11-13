# HEAD

- New memory layout for SWE coefficients. Only actual coefficients are now kept in memory. New property `Swe.num_of_coefficients` returns the actual number of coefficients. The API to access the coefficients remains unchanged.

# v0.1.0

- First release. Support for loading `.cut`, `grd`, and `.sph` files.
