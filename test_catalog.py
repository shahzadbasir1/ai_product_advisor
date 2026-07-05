from analysis.catalog_score import calculate_catalog_score
import inspect

print("=" * 60)
print("Function object:")
print(calculate_catalog_score)

print("\nSignature:")
print(inspect.signature(calculate_catalog_score))

print("\nArgument count:")
print(calculate_catalog_score.__code__.co_argcount)

print("\nVariable names:")
print(calculate_catalog_score.__code__.co_varnames)

print("\nDefaults:")
print(calculate_catalog_score.__defaults__)

print("=" * 60)