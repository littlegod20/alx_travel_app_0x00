from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing listings.
    
    Provides CRUD operations:
    - GET /api/listings/ - List all listings
    - GET /api/listings/{id}/ - Retrieve a specific listing
    - POST /api/listings/ - Create a new listing
    - PUT /api/listings/{id}/ - Update a listing (full update)
    - PATCH /api/listings/{id}/ - Update a listing (partial update)
    - DELETE /api/listings/{id}/ - Delete a listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed
    
    def get_queryset(self):
        """
        Optionally filter listings by query parameters.
        """
        queryset = Listing.objects.all()
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filter by country
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        # Filter by property type
        property_type = self.request.query_params.get('property_type', None)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Filter by max price
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            try:
                queryset = queryset.filter(price_per_night__lte=float(max_price))
            except ValueError:
                pass
        
        # Filter by active status (default to active only)
        is_active = self.request.query_params.get('is_active', 'true')
        if is_active.lower() == 'true':
            queryset = queryset.filter(is_active=True)
        elif is_active.lower() == 'false':
            queryset = queryset.filter(is_active=False)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """
        Custom action to get all bookings for a specific listing.
        GET /api/listings/{id}/bookings/
        """
        listing = self.get_object()
        bookings = Booking.objects.filter(listing=listing)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    
    Provides CRUD operations:
    - GET /api/bookings/ - List all bookings
    - GET /api/bookings/{id}/ - Retrieve a specific booking
    - POST /api/bookings/ - Create a new booking
    - PUT /api/bookings/{id}/ - Update a booking (full update)
    - PATCH /api/bookings/{id}/ - Update a booking (partial update)
    - DELETE /api/bookings/{id}/ - Delete a booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed
    
    def get_queryset(self):
        """
        Optionally filter bookings by query parameters.
        """
        queryset = Booking.objects.all()
        
        # Filter by guest
        guest_id = self.request.query_params.get('guest', None)
        if guest_id:
            queryset = queryset.filter(guest_id=guest_id)
        
        # Filter by listing
        listing_id = self.request.query_params.get('listing', None)
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by check-in date (after)
        check_in_after = self.request.query_params.get('check_in_after', None)
        if check_in_after:
            queryset = queryset.filter(check_in_date__gte=check_in_after)
        
        # Filter by check-out date (before)
        check_out_before = self.request.query_params.get('check_out_before', None)
        if check_out_before:
            queryset = queryset.filter(check_out_date__lte=check_out_before)
        
        return queryset

