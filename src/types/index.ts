export interface AIProvider {
  id: string;
  name: string;
  models: string[];
}

export interface AnalysisResult {
  anatomy?: Record<string, unknown>;
  metabolism?: Record<string, unknown>;
  intent?: Record<string, unknown>;
}

export interface GeneratedFile {
  path: string;
  content: string;
  type: 'json' | 'yaml' | 'markdown' | 'text';
}

export interface AppState {
  tier: 'free' | 'custom';
  provider: string;
  model: string;
  apiKey: string;
  anatomyInput: string;
  metabolismInput: string;
  intentInput: string;
  intentSelections: IntentSelections;
  analysisResult: AnalysisResult | null;
  generatedFiles: GeneratedFile[];
  readinessScore: number;
  isAnalyzing: boolean;
  isGenerating: boolean;
  currentStep: string;
  error: string | null;
}

export interface IntentSelections {
  techStack: string;
  primaryLanguage: string;
  designSystem: string;
  stateManagement: string;
  architecturalStyle: string;
}

export const TECH_STACKS = [
  'React + Node.js',
  'Next.js',
  'Vue + Express',
  'Angular + NestJS',
  'Svelte + Fastify',
  'Python + Flask',
  'Python + Django',
  'Go + Fiber',
  'Rust + Actix',
  'Ruby on Rails',
  'Other'
];

export const LANGUAGES = [
  'TypeScript',
  'JavaScript',
  'Python',
  'Go',
  'Rust',
  'Java',
  'C#',
  'Ruby',
  'PHP',
  'Other'
];

export const DESIGN_SYSTEMS = [
  'Custom/None',
  'Tailwind CSS',
  'Material UI',
  'Chakra UI',
  'Ant Design',
  'Shadcn/UI',
  'Bootstrap',
  'Radix UI',
  'Other'
];

export const STATE_MANAGEMENT = [
  'React Context',
  'Redux Toolkit',
  'Zustand',
  'Jotai',
  'Recoil',
  'MobX',
  'Vuex/Pinia',
  'None/Local State',
  'Other'
];

export const ARCHITECTURAL_STYLES = [
  'Monolith',
  'Microservices',
  'Serverless',
  'JAMstack',
  'Event-Driven',
  'Domain-Driven Design',
  'Clean Architecture',
  'MVC',
  'Other'
];
