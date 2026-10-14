const ADAM = "pNInz6obpgDQGcFmaJgB";
const RACHEL = "21m00Tcm4TlvDq8ikWAM";
const ANTONI = "ErXwobaYiN019PkySvjV";
const BELLA = "EXAVITQu4vr4xnSDxMaL";
const JOSH = "TxGEqnHWrfWFTfGW9XjX";
const ELLI = "MF3mGyEYCl7XYWbV9V6O";
const ARNOLD = "VR6AewLTigWG4xSOukaG";
const DOMI = "AZnzlk1XvdvUeBnXmlld";

export const DEFAULT_VOICE = ADAM;

export const VOICE_BY_TYPE: Record<string, string> = {
  industrial: ARNOLD,
  beach: BELLA,
  park: ELLI,
  academic: ANTONI,
  cultural_religious: JOSH,
  cultural_residential: DOMI,
  residential: RACHEL,
  commercial: ADAM,
  religious: JOSH,
  transportation: ANTONI,
};

export function voiceFor(type: string): string {
  return Object.prototype.hasOwnProperty.call(VOICE_BY_TYPE, type) ? VOICE_BY_TYPE[type] : DEFAULT_VOICE;
}
