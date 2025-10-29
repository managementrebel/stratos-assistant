
export type Role = 'user' | 'model';

export interface Message {
  role: Role;
  content: string;
  timestamp: Date;
  isError?: boolean;
}
