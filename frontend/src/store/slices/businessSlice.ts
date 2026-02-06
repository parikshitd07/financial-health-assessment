import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Business {
  id: number;
  business_name: string;
  industry: string;
  annual_revenue?: number;
}

interface BusinessState {
  businesses: Business[];
  selectedBusiness: Business | null;
  loading: boolean;
}

const initialState: BusinessState = {
  businesses: [],
  selectedBusiness: null,
  loading: false,
};

const businessSlice = createSlice({
  name: 'business',
  initialState,
  reducers: {
    setBusinesses: (state, action: PayloadAction<Business[]>) => {
      state.businesses = action.payload;
    },
    selectBusiness: (state, action: PayloadAction<Business>) => {
      state.selectedBusiness = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { setBusinesses, selectBusiness, setLoading } = businessSlice.actions;
export default businessSlice.reducer;
