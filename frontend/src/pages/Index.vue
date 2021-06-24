<template>
  <div class="q-pa-md bg-image">
    <q-page class="flex flex-top ecb-font-bold">
      <div class="fit row-xs wrap justify-start items-start content-start ">
        <div class="col-grow">
          <h3 style="color: white" align="center">Let us make your content understandable</h3>
          <h5 style="color: lightgrey" align="center">Senacor & Partners</h5>
        </div>
      </div>
      <div class="fit row wrap justify-center items-start content-start q-gutter-x-md">
        <div class="col-3">
          <q-card style="height: 300px">
            <q-card-section>
              <q-avatar rounded color="red" text-color="red"></q-avatar>
              <br>
              <h4 align="center">Setting up</h4>
              <div class="ecb-font-regular text-body1" align="center">Select the topic, summary length and your text file you want to summarize</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-3">
          <q-card style="height: 300px">
            <q-card-section>
              <q-avatar rounded color="blue" text-color="blue">2</q-avatar>
              <h4 align="center">Summarizing</h4>
              <div class="ecb-font-regular text-body1" align="center">Run our
                state-of-the-art summarization algorithms based on NLP technology
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-3">
          <q-card style="height: 300px">
            <q-card-section>
              <q-avatar rounded color="green" text-color="green">3</q-avatar>
              <br>
              <h4 align="center">Enjoying</h4>
              <div class="ecb-font-regular text-body1" align="center">Enjoy the new insights due to complexity reduction
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-page>
  </div>
</template>
<style>
.bg-image {
  background-image: url("../assets/background-landing.png");
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
<script>
export default {
  name: 'PageIndex'
}
</script>
