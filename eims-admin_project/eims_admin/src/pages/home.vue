<template>
  <div class= "ml-10 mt-5 text-start">
    <h1 class="font-inter font-bold text-4xl pb-1">Welcome, {{ userType }}</h1>
    <p class="font-inter font-bold text-gray-400">Check your latest updates</p>
    <hr class="w-[1100px] mt-2">
  </div>
  
  <!--Information Cards-->
  <div class="py-10 pl-10 flex flex-row space-x-10">
    <div class="flex">
      <div class="calendar-container w-[350px]">
        <VCalendar 
          :attributes="attrs"
          is-expanded
          :columns="1"
          borderless
        />
      </div>
    </div>
    <div class=""> <!-- Add padding to the dashboard -->
      <div class="border border-gray-300 rounded-lg shadow-lg p-4" style="height: 320px; width: 500px;">
        <apexchart 
          type="bar" 
          :options="barChartOptions" 
          :series="barChartSeries" 
        />
      </div>
    </div>
  </div>
  
  
  <!--Team's Progress -->
  <div class="flex space-x-10">
  
  
  
    
  <!---Events per Month Line Graph-->
  
  <div class="relative flex flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-lg border border-gray-300 h-[350px] w-full">
      <div class="relative mx-48 mt-4 flex flex-col gap-1 overflow-hidden rounded-none bg-transparent bg-clip-border text-gray-700 shadow-none md:flex-row md:items-center">
      </div>
      <div class="pt-0 px-2 pb-0 h-full">
        <div ref="lineChart"></div>
      </div>
    </div>
  
  
  </div>

   <div class="flex justify-center items-center w-full px-10 py-8">
    <div class="card w-full bg-white shadow-lg rounded-lg p-6">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Event Statistics</h2>
        <Chart type="line" :data="areaChartData" :options="areaChartOptions" class="h-[38rem] w-full" />
    </div>
   </div>
  
  
  
  
  
    </template>
    
    <script>
  import ApexCharts from 'apexcharts';
  import { defineComponent, onMounted, onUnmounted, ref } from 'vue';
  import VueApexCharts from "vue3-apexcharts";
  import axios from 'axios';
  import { Calendar } from 'v-calendar';
  import 'v-calendar/style.css';

  export default defineComponent({
    name: 'Dashboard',
    components: {
      apexchart: VueApexCharts,
      VCalendar: Calendar
    },
    data() {
      return {
        isDetailsVisible: false,
        attrs: [],
        events: [],
        userType: '',

        //Line chart configs
        barChartOptions: {
          chart: {
            type: 'bar',
             toolbar: {
                show: false,
                  },
          },
          plotOptions: {
              bar: {
                  columnWidth: '40%',
                  borderRadius: 2,
               },
           },
    dataLabels: {
      enabled: false, // Disable data labels
    },
          xaxis: {
            categories: [1, 2, 3, 4, 5], // Ratings
          },
          yaxis: {
            title: {
              text: 'No of users',
              style: {
                fontSize: '12px',
                fontWeight: 'bold',
                fontFamily: 'inherit',
              }
            },
            min: 0,
            labels: {
              formatter: function(value) {
                return parseInt(value);
              }
            },
            axisBorder: {
              show: true
            },
            axisTicks: {
              show: true
            },
            forceNiceScale: true,
            decimalsInFloat: 0
          },
          grid: {
            yaxis: {
              lines: {
                show: true
              }
            }
          },
          title: {
            text: 'Feedback Ratings',
            align: 'center',
            style: {
              fontSize: '18px',
              fontWeight: 'bold',
              fontFamily: 'inherit',
        
            },
          },
        },
        barChartSeries: [
          {
            name: 'Number of People',
            data: [2, 6, 14, 21, 24], // Number of people for each rating
          },
        ],
      };
    },
    methods: {
      toggleDetails() {
        this.isDetailsVisible = !this.isDetailsVisible;
      },
      async getUserType() {
        try {
          const userProfile = JSON.parse(localStorage.getItem('userProfile'));
          if (userProfile && userProfile.user_type) {
            this.userType = userProfile.user_type.charAt(0).toUpperCase() + userProfile.user_type.slice(1).toLowerCase();
            console.log('User type:', userProfile.user_type);
          } else {
            this.userType = 'User'; // fallback
          }
        } catch (error) {
          console.error('Error loading user profile:', error);
          this.userType = 'User'; // fallback
        }
      },
      async fetchFeedbackData() {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('No access token found');
            return;
          }
          
          const response = await axios.get('http://localhost:5000/api/feedback/statistics', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (response.data && Array.isArray(response.data)) {
            // Update the bar chart data
            this.barChartSeries[0].data = response.data;
          }
        } catch (error) {
          console.error('Error fetching feedback data:', error);
        }
      },
      async fetchEvents() {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('No access token found');
            return;
          }
          
          const response = await axios.get('http://localhost:5000/events/schedules', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (response.data && Array.isArray(response.data)) {
            this.events = response.data;
            this.attrs = this.events.map(event => ({
              key: event.events_id,
              dates: new Date(event.schedule),
              dot: {
                color: this.getEventColor(event.status),
                class: 'event-dot'
              },
              popover: {
                label: `${event.event_name} (${event.status})`
              }
            }));
            console.log('Calendar attributes:', this.attrs);
          }
        } catch (error) {
          console.error('Error fetching events:', error);
        }
      },
      getEventColor(status) {
        switch (status?.toLowerCase()) {
          case 'upcoming':
            return 'blue';
          case 'finished':
            return 'green';
          case 'cancelled':
            return 'red';
          case 'wishlist':
            return 'orange';
          default:
            return 'gray';
        }
      }
    },
    setup() {
      const date = ref(new Date());
      const isDatePickerDisabled = ref(false);
      const isDetailsVisible = ref(false);
      const selectedMonth = ref(null);
      const pollingInterval = ref(null);
      const lineChart = ref(null);
      
      // Area Chart Data
      const areaChartData = ref({
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: []
      });

      const colors = {
        'Wedding': { border: '#42A5F5', background: 'rgba(66, 165, 245, 0.2)' },
        'Birthday': { border: '#66BB6A', background: 'rgba(102, 187, 106, 0.2)' },
        'Christening': { border: '#FFA726', background: 'rgba(255, 167, 38, 0.2)' },
        'Anniversary': { border: '#EC407A', background: 'rgba(236, 64, 122, 0.2)' },
        'Corporate': { border: '#AB47BC', background: 'rgba(171, 71, 188, 0.2)' }
      };

      const getRandomColor = () => {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return {
          border: color,
          background: color.replace(')', ', 0.2)')
        };
      };

      const fetchEventsByMonth = async () => {
        try {
          const response = await axios.get('http://localhost:5000/events-by-month');
          const { eventTypes, data } = response.data;
          
          // Create a dataset for each event type
          const newDatasets = eventTypes.map(type => {
            // Use existing color if available, otherwise generate new one
            const color = colors[type] || getRandomColor();
            return {
              label: type,
              data: data[type],
              fill: true,
              borderColor: color.border,
              tension: 0.4,
              backgroundColor: color.background,
              hidden: false
            };
          });

          // Update datasets while preserving animations
          areaChartData.value.datasets = newDatasets;
        } catch (error) {
          console.error('Error fetching events by month:', error);
        }
      };

      const startPolling = () => {
        // Poll every 30 seconds
        pollingInterval.value = setInterval(fetchEventsByMonth, 30000);
      };

      const stopPolling = () => {
        if (pollingInterval.value) {
          clearInterval(pollingInterval.value);
          pollingInterval.value = null;
        }
      };

      const fetchCompletedEvents = async () => {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('No access token found');
            return;
          }

          const response = await fetch('http://localhost:5000/events/all', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            credentials: 'include'
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const events = await response.json();
          
          // Filter for completed events and group by month
          const completedEvents = events.filter(event => 
            event.status?.toLowerCase() === 'finished' && event.schedule
          );

          // Initialize counts for all months
          const monthlyCounts = Array(12).fill(0);

          // Count events by month
          completedEvents.forEach(event => {
            const date = new Date(event.schedule);
            const month = date.getMonth(); // 0-11
            monthlyCounts[month]++;
          });

          // Update the line chart
          if (lineChart.value) {
            const chartConfig = {
              series: [
                {
                  name: "Completed Events",
                  data: monthlyCounts,
                },
              ],
              chart: {
                type: "line",
                height: 240,
                toolbar: {
                  show: false,
                },
              },
              title: {
                text: "Completed Events by Month",
                align: "center",
                style: {
                  fontSize: "18px",
                  fontWeight: "bold",
                  fontFamily: "inherit",
                },
              },
              dataLabels: {
                enabled: false,
              },
              colors: ["#10B981"], // Green color for completed events
              stroke: {
                curve: 'smooth',
                width: 3,
              },
              markers: {
                size: 5,
                colors: ["#10B981"],
                strokeColors: "#fff",
                strokeWidth: 2,
              },
              xaxis: {
                axisTicks: {
                  show: false,
                },
                axisBorder: {
                  show: false,
                },
                labels: {
                  style: {
                    colors: "#616161",
                    fontSize: "12px",
                    fontFamily: "inherit",
                    fontWeight: 400,
                  },
                },
                categories: [
                  "Jan",
                  "Feb",
                  "Mar",
                  "Apr",
                  "May",
                  "Jun",
                  "Jul",
                  "Aug",
                  "Sep",
                  "Oct",
                  "Nov",
                  "Dec",
                ],
              },
              yaxis: {
                title: {
                  text: "Number of Events",
                  style: {
                    fontSize: "14px",
                    fontWeight: "500",
                    fontFamily: "inherit",
                  },
                },
                labels: {
                  style: {
                    colors: "#616161",
                    fontSize: "12px",
                    fontFamily: "inherit",
                    fontWeight: 400,
                  },
                  formatter: function(value) {
                    return Math.round(value);
                  }
                },
                min: 0,
                max: undefined,
                tickAmount: 5,
                forceNiceScale: true
              },
              grid: {
                show: true,
                borderColor: "#dddddd",
                strokeDashArray: 5,
                xaxis: {
                  lines: {
                    show: true,
                  },
                },
                padding: {
                  top: 5,
                  right: 20,
                },
              },
              fill: {
                opacity: 0.8,
                type: 'gradient',
                gradient: {
                  shade: 'dark',
                  gradientToColors: ['#34D399'],
                  shadeIntensity: 1,
                  type: 'horizontal',
                  opacityFrom: 1,
                  opacityTo: 1,
                },
              },
              tooltip: {
                theme: "dark",
                y: {
                  formatter: function(value) {
                    return Math.round(value) + " events";
                  }
                }
              },
            };

            const chart = new ApexCharts(lineChart.value, chartConfig);
            chart.render();
          }
        } catch (error) {
          console.error('Error fetching completed events:', error);
        }
      };

      onMounted(() => {
        fetchEventsByMonth();
        startPolling();
        fetchCompletedEvents();
      });

      onUnmounted(() => {
        stopPolling();
      });

      // Line Chart Options with click interaction
      const areaChartOptions = ref({
        plugins: {
          legend: {
            labels: {
              color: '#495057'
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#495057',
              callback: function(value, index) {
                const month = areaChartData.value.labels[index];
                const isSelected = selectedMonth.value === index;
                return isSelected ? ' ' + month : month;
              }
            },
            grid: {
              color: '#ebedef'
            }
          },
          y: {
            ticks: {
              color: '#495057'
            },
            grid: {
              color: '#ebedef'
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const clickedIndex = elements[0].index;
            selectedMonth.value = selectedMonth.value === clickedIndex ? null : clickedIndex;
            updateChartData(clickedIndex);
          }
        },
        hover: {
          mode: 'index',
          intersect: false
        }
      });

      const updateChartData = (monthIndex) => {
        if (selectedMonth.value === null) {
          // Show all months
          areaChartData.value.datasets.forEach(dataset => {
            dataset.hidden = false;
          });
        } else {
          // Show only selected month's data
          const selectedData = {};
          areaChartData.value.datasets.forEach(dataset => {
            selectedData[dataset.label] = dataset.data[monthIndex];
          });

          // Update datasets to show only selected month
          areaChartData.value.datasets.forEach(dataset => {
            const value = selectedData[dataset.label];
            dataset.data = Array(12).fill(null);
            dataset.data[monthIndex] = value;
          });
        }
      };

      return {
        date,
        isDatePickerDisabled,
        isDetailsVisible,
        areaChartData,
        areaChartOptions,
        selectedMonth,
        lineChart
      };
    },
    mounted() {
      this.fetchEvents();
      this.fetchFeedbackData();
      this.getUserType();
    }
  });
  
    </script>
    
    <style scoped>
     html {
      scroll-behavior: smooth;
    }

.calendar-container {
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  padding: 1rem;
}

.event-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

:deep(.vc-container) {
  --vc-font-family: 'Inter', sans-serif;
  --vc-rounded-lg: 0.5rem;
  --vc-header-padding: 10px 0;
  --vc-weeks-padding: 0 10px;
  --vc-day-padding: 5px 0;
  --vc-border-radius: 0.5rem;
  --vc-popover-content-padding: 0.5rem;
  --vc-popover-content-font-size: 0.875rem;
  --vc-popover-content-bg: white;
  --vc-popover-content-border: 1px solid #e2e8f0;
  --vc-popover-content-border-radius: 0.375rem;
  --vc-popover-content-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  --vc-today-bg: #f3f4f6;
  --vc-highlight-bg: #3b82f6;
  --vc-highlight-content-color: white;
  width: 100%;
}

:deep(.vc-header) {
  font-weight: 600;
}

:deep(.vc-day-content) {
  font-weight: 500;
}

:deep(.vc-day.is-today) {
  font-weight: bold;
}

:deep(.vc-day.is-not-in-month) {
  opacity: 0.4;
}

</style>