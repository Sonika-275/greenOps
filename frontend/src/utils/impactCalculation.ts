export const calculateTreesEquivalent = (co2Kg: number): number => {
  return co2Kg / 21; // ~21kg CO2 absorbed per tree per year
};

export const calculateCarKmEquivalent = (co2Kg: number): number => {
  return co2Kg * 4; // rough estimate
};

export const calculateLaptopDays = (co2Kg: number): number => {
  return co2Kg * 15; // approximate conversion
};
